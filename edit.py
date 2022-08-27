from ntpath import join
import os
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
            with open('fdt.txt', 'a') as f:
                f.write(message.content.split(f'{PREFIX}add ')[1] + '\n')
            await message.channel.send('Frage hinzugefügt!')
        if message.content.startswith(f'{PREFIX}remove '):
            index = message.content.split(f'{PREFIX}remove ')[1]
            with open('fdt.txt', 'r') as f:
                fdt = f.readlines()
            with open('fdt.txt', 'w') as f:
                f.writelines(fdt[:int(index)] + fdt[int(index)+1:])
            with open('geloescht.txt', 'a') as f:
                f.write(fdt[int(index)])
            await message.channel.send(f'Frage Nr: {index} entfernt!\n"{fdt[int(index)]}" wurde gelöscht')
        if message.content.startswith(f'{PREFIX}list'):
            with open('fdt.txt', 'r') as f:
                fdt = f.readlines()
            await message.channel.send(f"**Es sind {len(fdt)} Fragen in der Liste:**")
            for index, line in enumerate(fdt):
                await message.channel.send(f"**{index}:** {line}")
        if message.content.startswith(f'{PREFIX}edit '):
            index = message.content.split(f'{PREFIX}edit ')[1].split(' ')[0]
            new_message = message.content.split(f'{PREFIX}edit ')[
                1].split(' ')[1:]
            with open('fdt.txt', 'r') as f:
                fdt = f.readlines()
            with open('geloescht.txt', 'w') as f:
                f.write(fdt[int(index)])
            with open('fdt.txt', 'w') as f:
                f.writelines(
                    fdt[:int(index)] + [' '.join(new_message) + '\n'] + fdt[int(index)+1:])
            await message.channel.send(f'Frage Nr: {index} geändert!\n"{fdt[int(index)]}" wurde gelöscht')
        if message.content.startswith(f'{PREFIX}clear'):
            with open('fdt.txt', 'r') as f:
                fdt = f.readlines()
            with open('geloescht.txt', 'w') as f:
                for line in fdt:
                    f.write(line)
            with open('fdt.txt', 'w') as f:
                f.writelines('')
            await message.channel.send('Alle Fragen gelöscht!')
        if message.content.startswith(f'{PREFIX}help'):
            await message.channel.send(f'\
`{PREFIX}add <Frage>` - Fügt eine Frage hinzu\n\
`{PREFIX}remove <Nr>` - Entfernt eine Frage\n\
`{PREFIX}list` - Listet alle Fragen auf\n\
`{PREFIX}edit <Nr> <Frage>` - Ändert eine Frage\n\
`{PREFIX}clear` - Löscht alle Fragen')


bot.run(TOKEN)
