import os
from dotenv import load_dotenv
import discord

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command(name="add", description="Fügt eine Frage hinzu")
async def add(ctx, frage: str):
    with open('fdt.txt', 'a') as f:
        f.write(frage + '\n')
    await ctx.respond('Frage hinzugefügt!')

@bot.command(name="remove", description="Entfernt eine Frage")
async def remove(ctx, index: int):
    with open('fdt.txt', 'r') as f:
        fdt = f.readlines()
    with open('fdt.txt', 'w') as f:
        f.writelines(fdt[:int(index)] + fdt[int(index)+1:])
    with open('geloescht.txt', 'a') as f:
        f.write(fdt[int(index)])
    await ctx.respond(f"Frage Nr: {index} entfernt!")

@bot.command(name="list", description="Listet alle Fragen auf")
async def list(ctx):
    with open('fdt.txt', 'r') as f:
        fdt = f.readlines()
    await ctx.respond(f"**Es sind {len(fdt)} Fragen in der Liste:**")
    for index, line in enumerate(fdt):
        await ctx.send( f"**{index}:** {line}")

@bot.command(name="clear", description="Löscht alle Fragen")
async def clear(ctx):
    with open('fdt.txt', 'r') as f:
        fdt = f.readlines()
    with open('geloescht.txt', 'w') as f:
        for line in fdt:
            f.write(line)
    with open('fdt.txt', 'w') as f:
        f.writelines('')
    await ctx.respond('Alle Fragen gelöscht!')

@bot.command(name="edit", description="Ändert eine Frage")
async def edit(ctx, index: int, frage: str):
    with open('fdt.txt', 'r') as f:
        fdt = f.readlines()
    with open('geloescht.txt', 'w') as f:
        f.write(fdt[int(index)])
    with open('fdt.txt', 'w') as f:
        f.writelines(fdt[:int(index)] + [frage + "\n"] + fdt[int(index)+1:])
    await ctx.respond(f"Frage Nr: {index} geändert!")


bot.run(TOKEN)
