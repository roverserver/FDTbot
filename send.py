#!/usr/bin/env python3
from datetime import datetime
import os
import sys
from random import random
from dotenv import load_dotenv
import discord
import aiohttp
import asyncio

# get datapath from cliargs
DATA_PATH = sys.argv[1]

os.chdir(DATA_PATH)

load_dotenv()
# get webhook credentials from .env file
FDT_WEBHOOK = os.getenv('FDT_WEBHOOK_URL')
WARN_WEBHOOK = os.getenv('WARN_WEBHOOK_URL')
PING_ROLE_ID = os.getenv('PING_ROLE_ID')
TIMES_TO_WAIT = int(os.getenv('TIMES_TO_WAIT'))
BUFFER = int(os.getenv('BUFFER'))


async def webhook_send(message, url):
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(url, session=session)
        await webhook.send(message)


with open('fdt.txt', 'r') as f:
    fdt = f.readline()

if len(fdt) != 0:
    frage = fdt.split('\n')[0]
    message = f"<@&{PING_ROLE_ID}> {frage}"

    # send message to discord webhook
    asyncio.run(webhook_send(message, FDT_WEBHOOK))
    # print current time
    print(f"{datetime.now()} - sent fdt: {frage}")
    # delete first line from fdt.txt file and append it to archive.txt file
    with open('fdt.txt', 'r') as f:
        fdt = f.readlines()
    with open('archiv.txt', 'a') as f:
        f.write(fdt[0])
    with open('fdt.txt', 'w') as f:
        f.writelines(fdt[1:])
    with open('times_no_fdt.txt', 'w') as f:
        f.write(str(0))

    info = f"Frage gesendet. Es sind noch {len(fdt)-1} Fragen übrig"
if len(fdt) == 1:
    info = "Keine weiteren Fragen mehr! Wir brauchen eine neue Frage für Morgen"
if len(fdt) == 0:
    info = "Keine Fragen mehr! wir brauchen noch eine Frage für Heute\n\
Füge eine neue Frage mit !fdt <Frage> hinzu und versende sie mit f!send"
    with open('times_no_fdt.txt', 'r') as f:
        times_no_fdt = int(f.readline())
    if times_no_fdt >= TIMES_TO_WAIT and (times_no_fdt + 1) % (TIMES_TO_WAIT + 1) == 0:
        with open('archiv.txt', 'r') as f:
            archiv = f.readlines()
        if len(archiv) < BUFFER:
            print(f"{datetime.now()} - no more fdt, but archive is too small")
            asyncio.run(webhook_send(
                "Das Archiv ist zu klein um eine alte frage zu wählen", WARN_WEBHOOK))
        else:
            fdt = archiv[:BUFFER]
            frage = fdt[int(len(fdt) * random())]
            asyncio.run(webhook_send(
                f"Da seit {times_no_fdt} Tagen keine neue Frage mehr kam präsentiere ich ihnen eine alte <@&{PING_ROLE_ID}>\n{frage}", FDT_WEBHOOK))
            asyncio.run(webhook_send("Alte frage versendet", WARN_WEBHOOK))
            # print without newline
            print(f"{datetime.now()} - sent old fdt: {frage}", end="")
            with open('wiederholt.txt', 'a') as f:
                f.write(frage)
    else:
        print(f"{datetime.now()} - no new fdt for {times_no_fdt+1} days")

    with open('times_no_fdt.txt', 'w') as f:
        f.write(str(times_no_fdt+1))
    info = f"{info}\nseit {times_no_fdt+1} Tagen keine neue Frage mehr"
if len(fdt) <= 3:
    info = f"{info}\n<@&{PING_ROLE_ID}>"
asyncio.run(webhook_send(info, WARN_WEBHOOK))
