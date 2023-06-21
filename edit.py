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


def add_fdt(content: str):
    with open('fdt.txt', 'a') as f:
        f.write(content + '\n')
    with open('fdt.txt', 'r') as f:
        index = len(f.readlines()) - 1
    return f'Frage "{content}" an Stelle {index} hinzugefügt!'

def remove_fdt(index: int):
    with open('fdt.txt', 'r') as f:
        fragen = f.readlines()
    with open('fdt.txt', 'w') as f:
        f.writelines(fragen[:index] + fragen[index+1:])
    with open('geloescht.txt', 'a') as f:
        f.write(fragen[index])
    frage = fragen[index].strip('\n')
    return f'Frage Nr: {index} entfernt!\n "{frage}" wurde gelöscht'

def list_fdt():
    with open('fdt.txt', 'r') as f:
        fdt = f.readlines()
    return f'Es sind {len(fdt)} Fragen im Archiv\n' + ''.join([f'{index}: {frage}' for index, frage in enumerate(fdt)])

def edit_fdt(index: int, content: str):
    with open('fdt.txt', 'r') as f:
        fragen = f.readlines()
    deleted = fragen[index]
    with open('geloescht.txt', 'a') as f:
        f.write(deleted)
    fragen[index] = content + '\n'
    with open('fdt.txt', 'w') as f:
        f.writelines(fragen)
    deleted = deleted.strip('\n')
    return f'Frage Nr: {index} bearbeitet!\n"{deleted}" wurde durch "{content}" ersetzt'

def insert_fdt(index: int, content: str):
    with open('fdt.txt', 'r') as f:
        fdt = f.readlines()
    fdt.insert(index, content + '\n')
    with open('fdt.txt', 'w') as f:
        f.writelines(fdt)
    return f'Frage "{content}" an Stelle {index} eingefügt!'

def clear_fdt():
    with open('fdt.txt', 'r') as f:
        fdt = f.readlines()
    with open('geloescht.txt', 'a') as f:
        f.writelines(fdt)
    with open('fdt.txt', 'w') as f:
        f.write('')
    return 'Alle Fragen gelöscht!'

def send_fdt():
    process = subprocess.Popen(f'../send.py {DATA_PATH}', shell=True)
    process.wait()
    return 'Frage wurde gesendet!'

def help_fdt():
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


# old command handler
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # check if the message is in the control channel and starts with the prefix
    if message.channel.id == CONTROL_CHANNEL and message.content.startswith(PREFIX):
        command = message.content.split(' ')[0].split(PREFIX)[1]
        options = ' '.join(message.content.split(' ')[1:])

        if command == 'add':
            response = add_fdt(options)
        elif command == 'remove':
            response = remove_fdt(int(options))
        elif command == 'list':
            response = list()
        elif command == 'edit':
            response = edit_fdt(int(options.split(' ')[0]), ' '.join(options.split(' ')[1:]))
        elif command == 'insert':
            response = insert_fdt(int(options.split(' ')[0]), ' '.join(options.split(' ')[1:]))
        elif command == 'clear':
            response = clear_fdt()
        elif command == 'send':
            response = send_fdt()
        elif command == 'help':
            response = help_fdt()
        else:
            response = 'Unbekannter Befehl!\n' + help()

        await message.channel.send(response[:2000])

# slash command handler
@bot.command(description='Fügt eine Frage hinzu')
async def add(ctx, frage: discord.Option(str, 'Die Frage, die hinzugefügt werden soll')):
    print(f'/add: {frage}')
    await ctx.respond(add_fdt(frage))

@bot.command(description='Entfernt eine Frage')
async def remove(ctx, index: discord.Option(int, 'Der Index der Frage, die entfernt werden soll (siehe /list)')):
    print(f'/remove: {index}')
    await ctx.respond(remove_fdt(index))

@bot.command(description='Listet alle Fragen und ihre Indices auf')
async def list(ctx):
    print('/list')
    await ctx.respond(list_fdt()[:2000])

@bot.command(description='Bearbeitet eine Frage')
async def edit(ctx, index: discord.Option(int, 'Der Index der Frage, die bearbeitet werden soll (siehe /list)'), frage: discord.Option(str, 'Korrigierte Frage')):
    print(f'/edit: {index} {frage}')
    await ctx.respond(edit_fdt(index, frage))

@bot.command(description='Fügt eine Frage an einer bestimmten Stelle ein')
async def insert(ctx, index: discord.Option(int, "An welcher Stelle soll die Frage eingefügt werden?"), frage: discord.Option(str,'Die Frage, die hinzugefügt werden soll')):
    print(f'/insert: {index} {frage}')
    await ctx.respond(insert_fdt(index, frage))

@bot.command(description='Löscht alle Fragen')
async def clear(ctx):
    print('/clear')
    await ctx.respond(clear_fdt())

@bot.command(description='Sendet eine Frage')
async def send(ctx):
    print('/send')
    await ctx.respond(send_fdt())

print('Bot is connecting!')

bot.run(TOKEN)
