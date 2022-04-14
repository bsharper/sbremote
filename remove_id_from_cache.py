import os
import sys
import json
from sb_cache import SBRemoteCache

args = sys.argv[1:]

fname = "vidcache.json"

if len(args) == 0:
    bn = os.path.basename(sys.argv[0])
    print (f"Usage: python {bn} youtubeID\n")
    sys.exit(1)

sbcache = SBRemoteCache()
sbcache.remove_id_from_cache(args[0])


# txt = open(fname, "r").read()
# j = json.loads(txt)

# titles = j["titles"]
# new_titles = {}
# tfnd = False
# for t in titles:
#     obj = titles[t]
#     if obj["id"] == args[0]:
#         tfnd = True
#         print (f"Found segment entry for ID \"{args[0]}\"")
#     else:
#         new_titles[t] = obj

# if not tfnd:
#     print (f'ID "{args[0]}" not found in titles')

# sfnd = False
# new_segments = {}
# segments = j["segments"]
# for id in segments:
#     obj = segments[id]
#     if id == args[0]:
#         sfnd = True
#         print (f"Found segment entry for ID \"{id}\"")
#     else:
#         new_segments[id] = obj

# if not sfnd:
#     print (f'ID "{args[0]}" not found in segments')

# if (not sfnd) and (not tfnd):
#     print ("No changes to cache, cache not resaved")
#     sys.exit(0)

# new_cache = {"titles": new_titles, "segments": new_segments }
# backup_fname = f"{fname}.bak"
# with open(backup_fname, "w") as f:
#     f.write(txt)
# print (f"Saved backup file to {backup_fname}")

# with open(fname, "w") as f:
#     json.dump(new_cache, f)
# print (f"Cache saved to {fname}")