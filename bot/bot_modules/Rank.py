from .db import Sqlite
from .Request import get_wins_from_skycraft
from .htmltoimage import create_rank_image
from discord import File
from datetime import datetime
from discord.utils import get

class Rank:
    
    def __init__(self, db):
        self.db = db

    def reset(self): # it is to set wins to zero
        pass

    def show_wins(self, limit=False):
        if limit != False:
            res = self.db.query(f"select username, wins, img from rank order by wins desc limit {limit}")
            return res
        else:
            res = self.db.query(f"select r.username, r.wins, r.img, r.monthly_wins from rank as r join server_members as s on s.minecraft_nick=r.username order by monthly_wins desc")
            return res


    def recount(self, name_wins):
        result = self.db.query("select r.username, r.skywins, r.wins, monthly_wins from rank as r join server_members as s on s.minecraft_nick=r.username ")

        names = list(map(lambda a: a[0], result))

        skywins = list(map(lambda a: a[1], result))

        wins = list(map(lambda a: a[2], result))

        monthly_wins = list(map(lambda a: a[3], result))
        sql = ""
        for name in names:
            if name in name_wins["names"]:

                oldSkywins = int(str(skywins[names.index(name)]).replace(',', ''))
                newSkywins = int(name_wins["wins"][name_wins["names"].index(name)].replace(',', ''))
                if newSkywins < oldSkywins:
                    continue

                name_index = names.index(name)
                thisWins = int(wins[name_index])
                thisMonthlyWin = int(monthly_wins[name_index])

                sql += f"update rank set wins='{thisWins + (newSkywins-oldSkywins)}',monthly_wins='{thisMonthlyWin + (newSkywins-oldSkywins)}', skywins='{newSkywins}' where username='{name}';"

        
        self.db.queryScript(sql, True)

    def update(self):
        response1 = get_wins_from_skycraft(1)
        response2 = get_wins_from_skycraft(2)
        response3 = get_wins_from_skycraft(3)

        self.recount(response1)
        self.recount(response2)
        self.recount(response3)

        print('updated')

class RankCommands:

    def __init__(self, rank_tools, server):
        self.rank_tools = rank_tools
        self.server = server

    async def rank(self, ctx, page):
        if page.isnumeric() and int(page) < 200:

            page = int(page)

            datas = self.rank_tools.show_wins(False)
            try: # The lib that i use to create the image throw a error, but for some reason its create the image
                # then a use the try statament to ignore the error
                create_rank_image(datas, page)
            except:
                print('Image Excepted')
            
            await ctx.channel.send(file=File('rank.jpg'))
        else:
            await ctx.channel.send('Você digitou o comando da maneira errada ou o número da página está acima do suportado(199).')

    async def atualizar(self, ctx):
        self.rank_tools.update()
        await ctx.channel.send('Dados atualizados.')

    async def achar(self, ctx, name):
        datas = Sqlite.query(f"select wins from rank where username='{name}'")

        try:
            await ctx.channel.send(f'{name} : {datas[0][0]}')
        except:
            await ctx.channel.send('Esse nome não existe ou foi digitado de maneira incorreta!')
    
    async def rename(self, ctx, new_name):
        roles = []

        for role in ctx.author.roles:
            roles.append(role.name)

        if self.server.registed_role_name not in roles:
            await ctx.channel.send('Você precisa estar registrado!')
            return

        old_name = self.rank_tools.db.query(f"select r.username from rank as r join server_members as s on s.minecraft_nick=r.username where s.discord_name='{ctx.author.name}'", False)[0][0]

        print('old name', old_name)
        print('new name', new_name)

        self.rank_tools.db.query(f"update rank set username='{new_name}' where username='{old_name}'", True)
        self.rank_tools.db.query(f"update server_members set minecraft_nick='{new_name}' where minecraft_nick='{old_name}'", True)

        return True
        

class Server:
    def __init__(self):
        self.registed_role_name = "Registrado┃Top One"

    async def register(self, ctx, nick, mine_type, vip):
        if ctx.channel.name == '📞・registre-se':

            roles = []

            for role in ctx.author.roles:
                roles.append(role.name)

            if self.registed_role_name in roles:
                await ctx.channel.send('Você já está registrado!')
                return

            slq_query = Sqlite.query(f"select rank.username from rank where username='{nick}'")
            if slq_query == []:
                await ctx.channel.send('O nick de minecraft não existe!')
                return 
            
            if not (mine_type.lower() == 'original' or mine_type.lower() == 'pirata'):
                await ctx.channel.send('O tipo de conta de minecraft foi escrito de forma errada!')
                return           

            if vip.lower() not in ['esmeralda', 'ouro', 'diamante', 'nulo']:
                await ctx.channel.send('O vip foi digitado de maneira errada!')
                return 
            
            now_date = datetime.now()
            sql_date = f'{now_date.year}-{now_date.month}-{now_date.day}'

            Sqlite.query(f"insert into server_members(minecraft_nick, discord_id, mine_accont_type, register_date, vip) values ('{nick}', '{ctx.author.id}', '{mine_type}', '{sql_date}', '{vip}')", True)

            await ctx.channel.send(f'{ctx.author.name} registrado.')

            member = ctx.message.author
            role = get(member.guild.roles, name=self.registed_role_name)
            await member.add_roles(role)

    async def account(self, ctx):
        roles = []

        for role in ctx.author.roles:
            roles.append(role.name)

        if not self.registed_role_name in roles:
            return False
        
        account_info = Sqlite.query(f"select s.minecraft_nick, s.mine_accont_type, s.register_date, s.vip, r.wins, r.img, r.monthly_wins from server_members as s join rank as r on s.minecraft_nick=r.username where s.discord_id='{ctx.author.id}'", False)
        print(account_info)

        return account_info

    
server_tools = Server()
rank_tools = Rank(Sqlite)
rank_commands = RankCommands(rank_tools, server_tools)

if __name__ == "__main__":    
    pass