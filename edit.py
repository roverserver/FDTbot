import os
import subprocess
from dotenv import load_dotenv
import discord

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
CONTROL_CHANNEL = int(os.getenv('CONTROL_CHANNEL'))
PREFIX = os.getenv('PREFIX')

intents = discord.Intents.default()
intents.message_content = True


bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # check if the message is in the control channel
    if message.channel.id == CONTROL_CHANNEL:
        if message.content.startswith(f'{PREFIX}add '):
            with open('data/fdt.txt', 'a') as f:
                f.write(message.content.split(f'{PREFIX}add ')[1] + '\n')
            with open('data/fdt.txt', 'r') as f:
                index = len(f.readlines()) - 1
            await message.channel.send(f'Frage an Stelle {index} hinzugefügt!')
        if message.content.startswith(f'{PREFIX}remove '):
            index = message.content.split(f'{PREFIX}remove ')[1]
            with open('data/fdt.txt', 'r') as f:
                fdt = f.readlines()
            with open('data/fdt.txt', 'w') as f:
                f.writelines(fdt[:int(index)] + fdt[int(index)+1:])
            with open('data/geloescht.txt', 'a') as f:
                f.write(fdt[int(index)])
            frage = fdt[int(index)].strip('\n')
            await message.channel.send(f'Frage Nr: {index} entfernt!\n"{frage}" wurde gelöscht')
        if message.content.startswith(f'{PREFIX}list'):
            with open('data/fdt.txt', 'r') as f:
                fdt = f.readlines()
            await message.channel.send(f"**Es sind {len(fdt)} Fragen in der Liste:**")
            for index, line in enumerate(fdt):
                await message.channel.send(f"**{index}:** {line}")
        if message.content.startswith(f'{PREFIX}edit '):
            index = message.content.split(f'{PREFIX}edit ')[1].split(' ')[0]
            new_message = ' '.join(message.content.split(
                f'{PREFIX}edit ')[1].split(' ')[1:])
            with open('data/fdt.txt', 'r') as f:
                fdt = f.readlines()
            with open('data/geloescht.txt', 'w') as f:
                f.write(fdt[int(index)])
            with open('data/fdt.txt', 'w') as f:
                f.writelines(
                    fdt[:int(index)] + [new_message + '\n'] + fdt[int(index)+1:])
            frage = fdt[int(index)].strip('\n')
            await message.channel.send(f'Frage Nr: {index} geändert!\n"{frage}" wurde gelöscht')
        if message.content.startswith(f'{PREFIX}insert'):
            index = message.content.split(f'{PREFIX}insert ')[1].split(' ')[0]
            new_message = ' '.join(message.content.split(
                f'{PREFIX}insert ')[1].split(' ')[1:])
            with open('data/fdt.txt', 'r') as f:
                fdt = f.readlines()
            with open('data/fdt.txt', 'w') as f:
                f.writelines(
                    fdt[:int(index)] + [new_message + '\n'] + fdt[int(index):])
            await message.channel.send(f'Frage an Stelle {index} eingefügt!')
        if message.content.startswith(f'{PREFIX}clear'):
            with open('data/fdt.txt', 'r') as f:
                fdt = f.readlines()
            with open('data/geloescht.txt', 'w') as f:
                for line in fdt:
                    f.write(line)
            with open('data/fdt.txt', 'w') as f:
                f.writelines('')
            await message.channel.send('Alle Fragen gelöscht!')
        if message.content.startswith(f'{PREFIX}send'):
            process = subprocess.Popen('./send.sh', shell=True)
            process.wait()
            await message.channel.send('Frage versendet!')
        if message.content.startswith(f'{PREFIX}help'):
            await message.channel.send(f'\
`{PREFIX}add <Frage>` - Fügt eine Frage hinzu\n\
`{PREFIX}remove <Nr>` - Entfernt eine Frage\n\
`{PREFIX}list` - Listet alle Fragen auf\n\
`{PREFIX}edit <Nr> <Frage>` - Ändert eine Frage\n\
`{PREFIX}insert <Nr> <Frage>` - Fügt eine Frage an dieser Stelle ein\n\
`{PREFIX}clear` - Löscht alle Fragen\n\
`{PREFIX}send` - Sendet eine Frage des Tages manuell')


bot.run(TOKEN)
