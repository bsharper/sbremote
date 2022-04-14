import json
import humanize

lns = [ x for x in open("skips.json").read().replace("}{", "}\n{").replace("} {", "}\n{").split('\n') if len(x) > 0 ]
t=0
for ln in lns:
    try:
        j = json.loads(ln)        
        t += j["duration"]
    except json.decoder.JSONDecodeError:
        print (f"Could not parse {ln}")
        continue

print (f"{humanize.naturaldelta(t)} ({int(t)} seconds)")
