import os
import re

import discord
from dotenv import load_dotenv

from manage_data import manage
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
                if page > 20:
                    await msg.channel.send('Páginas maiores que 20 não estão disponivéis ainda.')
                    return
            except:
                page = int(msg.content[6])
        except:
            await msg.channel.send("Escreva da maneira correta §rank <página>")

        datas = manage.show_wins(False)
        datas = datas[(page-1)*20:page*(20)]

        message_of_wins = ''
        for row in datas:
            message_of_wins += (f'User {row[0]}, Vitórias {row[1]}\n')

        await msg.channel.send(message_of_wins)
    
    if msg.content == '§update':
        update()
        await msg.channel.send('Dados atualizdos')



client.run(TOKEN)