import os
import re

import discord
from dotenv import load_dotenv
from discord.ext.commands import Bot

from manage_data import manage
from db import Sqlite
from interface import update_datas

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

PREFIX = '§'

client = discord.Client()

bot = Bot(command_prefix = PREFIX)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command()
async def comandos(ctx):
    embed = discord.Embed(title="Lista de Comandos", description=f"Uma lista dos Comandos disponíveis", color=0xff1a1a)

    comandos = f"""```
rank <página> | mostra o rank de vitorias;
achar <nome_de_usuario> | mostra as vitórias do jogador marcado;
atualizar | atualiza o rank;
sourcecode | indisponível nesse momento;
criadores | mostra os criadores do bot
```    
"""

    embed.add_field(name="Comando    Função", value=comandos)

    await ctx.channel.send(embed=embed)

@bot.command()
async def rank(ctx, page):
    if page.isnumeric() and int(page) < 61:

        page = int(page)

        datas = manage.show_wins(False)
            
        datas = datas[(page-1)*20:page*(20)]

        message_of_wins = ''
        for row in datas:
            message_of_wins += (f'{row[0]} | {row[1]}\n')

        embed = discord.Embed(title="Vitórias dos Jogadores", description=f"Rank das vitórias página {page}", color=0xff1a1a)
        embed.add_field(name="Nome    Vitórias", value=message_of_wins)
        embed.set_image(url='https://skycraft.com.br/images/games/blockparty.png')

        await ctx.channel.send(embed=embed)
    else:
        await ctx.channel.send(str(ctx.author.mention) + ', você escreveu o parâmetro do comando de maneira incorreta.')

@bot.command()
async def atualizar(ctx):
    update_datas()
    await ctx.channel.send('Dados atualizados.')

@bot.command()
async def achar(ctx, name):
    datas = Sqlite.query(f"select wins from rank where username='{name}'")

    try:
        await ctx.channel.send(f'{name} : {datas[0][0]}')
    except:
        await ctx.channel.send('Esse nome não existe ou foi digitado de maneira incorreta!')
"""
@bot.command()
async def sourcecode(ctx):
    await ctx.channel.send('https://github.com/gustatramontin/skycraft_wins_counter/tree/master')

"""

@bot.command()
async def criadores(ctx):
    await ctx.author.send('Os criadores são NewNeo #6326 e panther #5721.')

bot.run(TOKEN)
