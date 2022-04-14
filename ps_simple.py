import os
import re
import sys
import json
import time
import pyatv
import random
import asyncio

pair = pyatv.pair
Protocol = pyatv.const.Protocol

output_filename = "appletv.json"

loop = asyncio.get_event_loop()

async def scan():
    print ("Scanning...", end="", flush=True)
    atvs = await pyatv.scan(loop)
    print ("done", flush=True)

    print ("Select the number for the ATV to pair with:\n")
    ar = {}
    names = {}
    for i, atv in enumerate(atvs):
        n = i+1
        ar[str(n)] = atv
        name = f"{atv.name} ({atv.address})"
        names[str(n)] = name
        print(f"{n}) {name}")
    ans = "-1"
    while ans not in ar.keys():
        ans = input("> ")
    atv = ar[ans]
    name = names[ans]
    print ("pairing atv %s" % (atv))
    pairing = await pair(atv, Protocol.AirPlay, loop)
    await pairing.begin()
    print ("Enter pairing code on screen")
    code = input ("Pairing code: ")
    pairing.pin(code)
    await pairing.finish()
    if pairing.has_paired:
        print("Paired with device!")
        print("Credentials:", pairing.service.credentials)
    else:
        print("Did not pair with device!")
    creds = pairing.service.credentials
    id = atv.identifier
    nj = {"credentials": creds, "identifier": id, "name": name}
    json.dump(nj, open(output_filename, "w"))

loop.run_until_complete(scan())
loop.close()