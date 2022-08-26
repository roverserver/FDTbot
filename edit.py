import os
from dotenv import load_dotenv
import discord

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
CONTROL_CHANNEL = os.getenv('CONTROL_CHANNEL')

intents = discord.Intents.default()
intents.message_content = True


client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('f!add '):
        await message.channel.send('Nachricht hinzugefügt!')
        with open('fdt.txt', 'a') as f:
            f.write(message.content.split('f!add ')[1] + '\n')
    if message.content.startswith('f!remove '):
        index = message.content.split('f!remove ')[1]
        await message.channel.send('Nachricht Nr: ' + index + ' entfernt!')
        with open('fdt.txt', 'r') as f:
            fdt = f.readlines()
        with open('fdt.txt', 'w') as f:
            f.writelines(fdt[:int(index)] + fdt[int(index)+1:])
    if message.content.startswith('f!list'):
        await message.channel.send('**Liste der Nachrichten:**')
        with open('fdt.txt', 'r') as f:
            fdt = f.readlines()
        for index, line in enumerate(fdt):
            await message.channel.send( str(index) + ': ' + line)

client.run(TOKEN)
