import os
import subprocess
from dotenv import load_dotenv
import discord

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
CONTROL_CHANNEL = int(os.getenv('CONTROL_CHANNEL'))
PREFIX = os.getenv('PREFIX')

DATA_PATH = "data"

os.makedirs(DATA_PATH, exist_ok=True)
os.chdir(DATA_PATH)
intents = discord.Intents.default()
intents.message_content = True


bot = discord.Bot(intents=intents)


def add(content: str):
    with open('fdt.txt', 'a') as f:
        f.write(content + '\n')
    with open('fdt.txt', 'r') as f:
        index = len(f.readlines()) - 1
    return f'Frage an Stelle {index} hinzugefügt!'

def remove(index: int):
    with open('fdt.txt', 'r') as f:
        fdt = f.readlines()
    with open('fdt.txt', 'w') as f:
        f.writelines(fdt[:index] + fdt[index+1:])
    with open('geloescht.txt', 'a') as f:
        f.write(fdt[index])
    frage = fdt[index].strip('\n')
    return f'Frage Nr: {index} entfernt!\n "{frage}" wurde gelöscht'

def list():
    with open('fdt.txt', 'r') as f:
        fdt = f.readlines()
    return f'Es sind {len(fdt)} Fragen im Archiv\n' + ''.join([f'{index}: {frage}' for index, frage in enumerate(fdt)])

def first2k(text: str):
    """returns the first 2000 characters of a message"""
    return text[:2000]

def edit(index: int, content: str):
    with open('fdt.txt', 'r') as f:
        fdt = f.readlines()
    deleted = fdt[index]
    with open('geloescht.txt', 'a') as f:
        f.write(deleted)
    fdt[index] = content + '\n'
    with open('fdt.txt', 'w') as f:
        f.writelines(fdt)
    deleted = deleted.strip('\n')
    return f'Frage Nr: {index} bearbeitet!\n"{deleted}" wurde gelöscht'

def insert(index: int, content: str):
    with open('fdt.txt', 'r') as f:
        fdt = f.readlines()
    fdt.insert(index, content + '\n')
    with open('fdt.txt', 'w') as f:
        f.writelines(fdt)
    return f'Frage an Stelle {index} eingefügt!'

def clear():
    with open('fdt.txt', 'r') as f:
        fdt = f.readlines()
    with open('geloescht.txt', 'a') as f:
        f.writelines(fdt)
    with open('fdt.txt', 'w') as f:
        f.write('')
    return 'Alle Fragen gelöscht!'

def send():
    process = subprocess.Popen(f'../send.py {DATA_PATH}', shell=True)
    process.wait()
    return 'Frage wurde gesendet!'

def help():
    return f'`{PREFIX}add <Frage>` - Fügt eine Frage hinzu\n \
`{PREFIX}remove <index>` - Entfernt eine Frage\n \
`{PREFIX}list` - Listet alle Fragen auf\n \
`{PREFIX}edit <index> <Frage>` - Bearbeitet eine Frage\n \
`{PREFIX}insert <index> <Frage>` - Fügt eine Frage an einer bestimmten Stelle ein\n \
`{PREFIX}clear` - Löscht alle Fragen\n \
`{PREFIX}send` - Sendet eine Frage\n \
`{PREFIX}help` - Zeigt diese Hilfe an'


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # check if the message is in the control channel and starts with the prefix
    if message.channel.id == CONTROL_CHANNEL and message.content.startswith(PREFIX):
        command = message.content.split(' ')[0].split(PREFIX)[1]
        options = ' '.join(message.content.split(' ')[1:])

        if command == 'add':
            response = add(options)
        elif command == 'remove':
            response = remove(int(options))
        elif command == 'list':
            response = list()
        elif command == 'edit':
            response = edit(int(options.split(' ')[0]), ' '.join(options.split(' ')[1:]))
        elif command == 'insert':
            response = insert(int(options.split(' ')[0]), ' '.join(options.split(' ')[1:]))
        elif command == 'clear':
            response = clear()
        elif command == 'send':
            response = send()
        elif command == 'help':
            response = help()
        else:
            response = 'Unbekannter Befehl!\n' + help()

        await message.channel.send(first2k(response))

print('Bot is connecting!')

bot.run(TOKEN)
