import os
import re

import discord
from dotenv import load_dotenv

from manage_data import manage
from db import Sqlite
from interface import update

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(msg):
    if msg.author == client.user:
        return
    
    if re.search('^§rank ', msg.content):
        try:
            try:
                page = int(msg.content[6:8])
                if page > 61:
                    await msg.channel.send('Páginas maiores que 61 não estão disponivéis ainda.')
                    return
            except:
                page = int(msg.content[6])
        except:
            await msg.channel.send("Escreva da maneira correta §rank <página>")

        datas = manage.show_wins(False)
        
        datas = datas[(page-1)*20:page*(20)]

        message_of_wins = ''
        for row in datas:
            message_of_wins += (f'{row[0]} | {row[1]}\n')


        embed = discord.Embed(title="Vitórias dos Jogadores", description=f"Rank das vitórias página {page}", color=0xff1a1a)
        embed.add_field(name="Nome    Vitórias", value=message_of_wins)
        embed.add_field(name="AD", value="Inscreva-se no Canal do Felipe Neto: https://www.youtube.com/felipeneto/")

        await msg.channel.send(embed=embed)

    if re.search('^§find ', msg.content):

        name = msg.content[6:]
        datas = Sqlite.query(f"select wins from rank where username='{name}'")
        try:
            await msg.channel.send(f'{name} : {datas[0][0]}')
        except:
            await msg.channel.send('Esse nome não existe ou foi digitado de maneira incorreta!')
    
    if msg.content == '§update':
        update()
        await msg.channel.send('Dados atualizados.')


client.run(TOKEN)
