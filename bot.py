import os
import re

import discord
from dotenv import load_dotenv
from discord.ext.commands import Bot

from manage_data import manage
from db import Sqlite
from interface import update_datas

from karma import add_member, get_karma_data, check_date, add_karma, get_karma_by_name

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

PREFIX = '§'

client = discord.Client()
intents = discord.Intents(messages=True, guilds=True, members=True)

bot = Bot(command_prefix=PREFIX, intents=intents)

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

@bot.command()
async def karma(ctx, sign=None,name=None):

    author = ctx.author.name
    try:
        name = bot.get_user(int(name[3:-1])).name
        print(name)
    except:
        await ctx.channel.send('**Digite o comando da maneira certa.**')
        return

    raw_data = get_karma_data()

    members = []
    dates = []

    for data in raw_data:
        members.append(data[0])
        dates.append(data[2])

    if name==None or name not in members or sign==None:
        await ctx.channel.send('**Digite o comando da maneira certa.**')

    elif name == ctx.author.name:
        await ctx.channel.send('**Você não pode dar karma a si mesmo.**')

    elif sign == '+' or sign == '-':
        try:
            valid_date = check_date(dates[members.index(author)])
        except ValueError:
            await ctx.channel.send('**Você usuário não esta no banco.**')

        if valid_date:
            add_karma(name, sign, author)
            await ctx.channel.send('**O karma foi adicionado.**')
        else:
            await ctx.channel.send('**Só pode adicionar depois de dois dias depois do seu último karma.**')

@bot.command()
async def karmatop(ctx):
    raw_data = get_karma_data()[:30]

    message = ''

    for data in raw_data:
        message += f'{data[0]} | {data[1]}\n'

    embed = discord.Embed(title="Lista de Karmas", description="Nome e karma de cada usuário do servidor.", color=0xff1a1a)
    embed.add_field(name="Nome    Karma", value=message)

    await ctx.channel.send(embed=embed)

@bot.command()
async def karmaver(ctx, name):
    karma = get_karma_by_name(name)

    if karma != None:
        await ctx.channel.send(f'**O karma de {name} é {karma}.**')
    else:
        await ctx.channel.send('**Digite um nome válido.**')

    

@bot.command()
async def karmamembersadd(ctx):
    members = ctx.guild.members

    for member in members:
        if not member.bot:
            add_member(member.name)

bot.run(TOKEN)
