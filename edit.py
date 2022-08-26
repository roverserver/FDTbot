import os
from dotenv import load_dotenv
import discord

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True


client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


#add question to fdt.txt file
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!add '):
        await message.channel.send('Added!')
        with open('fdt.txt', 'a') as f:
            f.write(message.content.split('!add ')[1] + '\n')

client.run(TOKEN)
