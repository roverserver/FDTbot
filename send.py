import os
from dotenv import load_dotenv
import discord

load_dotenv()
#get webhook credentials from .env file
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

#get webhook id and token from url
WEBHOOK_ID = WEBHOOK_URL.split('/')[-2]
WEBHOOK_TOKEN = WEBHOOK_URL.split('/')[-1]

# PING_ROLE_ID = os.getenv('PING_ROLE_ID')
# webhook = discord.Webhook.from_url(WEBHOOK_URL, adapter=discord.AsyncWebhookAdapter(discord.AsyncWebhookAdapter(discord.Client())))

# open fdt.txt file and get first line
with open('fdt.txt', 'r') as f:
    fdt = f.readline()


message = '**' + fdt.split('\n')[0] + '**'

#send message to discord webhook
# client.send(message)

print(message)

#delete first line from fdt.txt file and append it to archive.txt file
with open('fdt.txt', 'r') as f:
    fdt = f.readlines()
with open('archiv.txt', 'a') as f:
    f.write(fdt[0])
with open('fdt.txt', 'w') as f:
    f.writelines(fdt[1:])

