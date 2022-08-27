import os
from dotenv import load_dotenv
import discord
import aiohttp
import asyncio


load_dotenv()
#get webhook credentials from .env file
FDT_WEBHOOK = os.getenv('FDT_WEBHOOK_URL')
WARN_WEBHOOK = os.getenv('WARN_WEBHOOK_URL')
PING_ROLE_ID = os.getenv('PING_ROLE_ID')

async def webhook_send(message, url):
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(url, session=session)
        await webhook.send(message)
# open fdt.txt file and get first line
with open('fdt.txt', 'r') as f:
    fdt = f.readline()

if len(fdt) != 0:
    message = f"<@&{PING_ROLE_ID}> " + fdt.split('\n')[0]

    #send message to discord webhook
    asyncio.run(webhook_send(message, FDT_WEBHOOK))
    #delete first line from fdt.txt file and append it to archive.txt file
    with open('fdt.txt', 'r') as f:
        fdt = f.readlines()
    with open('archiv.txt', 'a') as f:
        f.write(fdt[0])
    with open('fdt.txt', 'w') as f:
        f.writelines(fdt[1:])
    
    info = f"Frage gesendet. Es sind noch {len(fdt)-1} Fragen übrig"
    if len(fdt) == 1:
        info = "Keine weiteren Fragen mehr! Wir brauchen eine neue Frage für Morgen"
    if len(fdt) == 0:
        info = "Keine Fragen mehr! wir brauchen noch eine Frage für Heute"
    if len(fdt) <= 3:
        info = f"{info}\n<@&{PING_ROLE_ID}>"
    asyncio.run(webhook_send(info, WARN_WEBHOOK))


