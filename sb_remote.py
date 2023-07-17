import os
import re
import sys
import json
import time
import pyatv
import random
import asyncio
from pyatv.const import InputAction
Protocol = pyatv.const.Protocol

from sb_cache import SBRemoteCache

from singleton import SingleInstance

try:
    me = SingleInstance()
except:
    time.sleep(0.1)
    sys.exit(-1)


skip_types = ["sponsor", "selfpromo", "intro", "outro"]
proj_name = "SBRemote"
proj_version = "0.2"
janky_restart = True
announce_skips = True

if not os.path.exists("restart.sh"):
    janky_restart = False

def write_saynow():
    if not os.path.exists("saynow.sh") and sys.platform == "darwin":
        fn="saynow.sh"
        print (f"Creating file \"{fn}\"")
        s="""#!/bin/bash
read -r -d '' VOICES <<- EOM
Alex
Daniel
Fred
Karen
Moira
Rishi
Samantha
Tessa
Veena
Victoria
EOM
DT=$(date +%k)
TAILTXT=""
if [[ $(($(($RANDOM%10))%2)) == 1 ]]; then
  TAILTXT=", you got skipped"
fi
if [[ $DT -gt 8 && $DT -lt 23 ]]; then
  v=$(echo "$VOICES" | sort -R | tail -1)
  say -v "$v" "Move off ${1}${TAILTXT}" & 
fi
"""
        open(fn, "w").write(s)
        import stat
        st = os.stat(fn)
        os.chmod(fn, st.st_mode | stat.S_IEXEC)

def restart_script():
    """ This is a bad way to do things, but until all stalling bugs are fixed, it's better than nothing """
    os.system(f"./restart.sh {os.getpid()}")

def simplify_segments(segments):
    """ Throw away a bunch of the interformation in the skip segments to keep things simple """
    na = []
    for s in segments:
        obj = [s["category"], s["segment"][0], s["segment"][1]]
        na.append(obj)
    
    na = [ x for x in na if x[0] in skip_types ]
    return na

def merge_segments (segments, first_index, second_index):
    """ Some segments we want to skip are overlapping, to prevent underskipping or unnecessary skips, we merge the segments"""
    new_segments = []
    for i, s in enumerate(segments):
        if i != first_index and i != second_index:
            new_segments.append(s)
    s = segments[first_index]
    c = segments[second_index]
    nsegment = [ s[0], min(s[1], c[1]), max(s[2], c[2]), f"merged from {s[0]} and {c[0]}"]
    print (f"Merged {s} and {c} to {nsegment}")
    new_segments.append(nsegment)
    new_segments.sort(key = lambda x: x[1])

    return new_segments


def check_overlaps (segments):
    """ Merged skips might need to be merged even more, this keeps merging until no more overlaps exist """
    all_good = False
    while not all_good:
        first_index, second_index = -1, -1
        for o, s in enumerate(segments):
            for i, c in enumerate(segments):
                if s[1] < c[1] and s[2] < c[2] and s[2] > c[1]:
                    print (f"Overlap {s} {c}")
                    first_index = o
                    second_index = i
                    break
            if first_index > -1 or second_index > -1:
                break
        
        if first_index > -1 or second_index > -1:
            segments = merge_segments(segments, first_index, second_index)
        else:
            all_good = True
    
    return segments

def manage_segments(segments):
    segments = simplify_segments(segments)
    segments = check_overlaps(segments)
    return segments


def near_skip (segments, position):
    for s in segments:
        diff = float(s[1]) - float(position)
        if diff > 0.0 and diff < 3.0:
            return diff
    return False
                 
async def do_skip_now (segments, position, remote):
    for s in segments:
        if round(s[1]) == int(position) or (position < 5 and s[1] == 0 and (s[2]-position > 2)):
            padding = s[1] - int(s[1])
            prewait = 0.0
            if announce_skips and sys.platform == "darwin":
                write_saynow()
                os.system('./saynow.sh "%s"' % (s[0]))
            if padding > 0.1:
                prewait = padding * 0.8

            print ("Skipping '%s' from %d to %d (%.2f prewait)" % (s[0], s[1], s[2], prewait))
            
            if prewait > 0.0:
                await asyncio.sleep(prewait)
            await remote.set_position(int(s[2]))
            return s
    return False
        
def print_state(txt):
    lns = txt.split("\n")
    headers = ['Media type', 'Device state', 'Title', 'Artist', 'Album', 'Position', 'Repeat', 'Shuffle']
    enabled_headers = ['Device state', 'Title', 'Artist', 'Position']
    for ln in lns:
        if any([ x for x in enabled_headers if x in ln ]):
            print (ln)

async def connect_atv():
    while not os.path.exists("/data/appletv.json"):
        from pair_and_save import scan
        await scan(loop)
    
    data = json.load(open('/data/appletv.json'))

    id = data["identifier"]
    creds = data["credentials"]
    if "name" in data.keys():
        print (f"Connecting to {data['name']}...", end="", flush=True)
    else:
        print (f"Connecting to ATV ({id})...", end="", flush=True)
    stored_credentials = { Protocol.AirPlay: creds }
    atvs = await pyatv.scan(loop, identifier=id)
    atv = atvs[0]
    for protocol, credentials in stored_credentials.items():
        atv.set_credentials(protocol, credentials)
    try:
        device = await pyatv.connect(atv, loop)
        remote = device.remote_control
        print ("done", flush=True)
        return device, remote
    except Exception as ex:
        print ("error\nFailed to connect: %s" % (ex))
        return None, None
    


async def main_loop():
    runstart = time.time()
    sbrcache = SBRemoteCache(debug=True)
    device, remote = await connect_atv()
    if device == None or remote == None:
        print ("Could not connect to ATV. Try again or attempt pairing again using pair_and_save.py\n")
        sys.exit(0)

    last_state = ""
    hold_count = 0
    restart_time = 900
    sleep_time = 1.0
    v = {}
    last_hl = ""
    id = ""
    is_near_skip = False
    segments = []
    skipped_segments = []
    remove_segment_after_skip = True
    while True:
        sys.stdout.flush()
        sys.stderr.flush()
        if janky_restart:
            runtime = time.time() - runstart
            if runtime > restart_time-10:
                print ("Nearing restart")
            if runtime > restart_time and not is_near_skip:
                restart_script()
        
        await asyncio.sleep(sleep_time)
        
        waiting_result = True
        
        while waiting_result:
            try:
                wp = await asyncio.wait_for(device.metadata.playing(), 3)
                waiting_result = False
            except asyncio.TimeoutError:
                print ("Timed out, attempting reconnect")
                dt = str(time.ctime())
                open('timeouts_log.txt', 'a').write(f"{dt} Timed out\n")
                await asyncio.sleep(sleep_time)
                device, remote = await connect_atv()
                    
        app = device.metadata.app
        hl = f"{wp.artist} {wp.title}"
        if app == None: continue
        is_youtube = app.identifier == "com.google.ios.youtube"
        is_playing = str(wp.device_state) == "DeviceState.Playing"
        is_none_none = hl == "None None"
        state = f"{app.identifier} {wp.artist} {wp.title} {wp.device_state}"
        state_changed = state == last_state

        if is_youtube and (not is_none_none):
            if hl != last_hl:
                try:
                    v = sbrcache.lookup_video(wp.artist, wp.title)
                    id = v["video"]["id"]
                    segments = manage_segments(v["segments"])
                    skipped_segments = []
                except Exception as ex:
                    print (f"Error during lookup: {ex}")
                    segments = {}
                    skipped_segments = []

            last_hl = hl            
            stxt = json.dumps(segments)
            if state_changed or hold_count == 0:
                print_state(str(wp))
                print ("{:>13} {:}".format("ID:", id))
                print ("{:>13} {:}".format("Segments:", stxt))
                if len(skipped_segments) > 0:
                    print ("{:>13} {:}".format("Skipped:", skipped_segments))
                print ("")
                hold_count = 5
            else:
                if hold_count > 0:
                    hold_count -= 1

            if is_playing:
                is_near_skip = False
                if near_skip(segments, wp.position):
                    is_near_skip = True
                    print ("========== Approaching skip ==========")
                    sleep_time = 0.5
                else:
                    sleep_time = 1
                
                did_skip = await do_skip_now(segments, wp.position, remote)
                if did_skip:
                    print ("*"*80)
                    print ("We skipped something, yeah!".center(80))
                    print ("*"*80)
                    if remove_segment_after_skip:
                        segments.remove(did_skip)
                        skipped_segments.append(did_skip)
                    duration = did_skip[2] - did_skip[1]
                    #skip_record = {"video": hl, "duration": duration, "id": id, "segment": did_skip}
                    skip_record = {"id": id, "duration": duration, "segment": did_skip}
                    with open("skips.json", "a") as outf:
                        json.dump(skip_record, outf)
                        outf.write("\n")

def banner():
    width = 60
    print ("="*width)
    proj_txt = f"{proj_name} v{proj_version}".center(width)
    print (proj_txt)
    print ("="*width)

async def main():
    banner()
    await main_loop()

if __name__ == "__main__":
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
