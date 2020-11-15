from .db import Sqlite
from .Request import get_wins_from_skycraft
from .htmltoimage import create_rank_image
from discord import File

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
            res = self.db.query(f"select username, wins, img from rank order by wins desc")
            return res


    def recount(self, name_wins):
        result = self.db.query("select username, skywins, wins from rank")

        names = list(map(lambda a: a[0], result))

        skywins = list(map(lambda a: a[1], result))

        wins = list(map(lambda a: a[2], result))
        sql = ""
        for name in names:
            if name in name_wins["names"]:

                oldSkywins = int(str(skywins[names.index(name)]).replace(',', ''))
                newSkywins = int(name_wins["wins"][name_wins["names"].index(name)].replace(',', ''))
                if newSkywins < oldSkywins:
                    continue

                name_index = names.index(name)
                thisWins = int(wins[name_index])
                sql += f"update rank set wins='{thisWins + (newSkywins-oldSkywins)}', skywins='{newSkywins}' where username='{name}';"

                #self.db.query(f"update rank set wins='{thisWins + (newSkywins-oldSkywins)}', skywins='{newSkywins}' where username='{name}'", True)
        
        self.db.queryScript(sql, True)
    def rename(self, old_name, new_name):
        try:
            self.db.query(f"update rank set username='{new_name}' where username='{old_name}'", True)
            return True
        except:
            return False

    
    def update(self):
        response = get_wins_from_skycraft()

        self.recount(response)
        print('updated')

class RankCommands:

    def __init__(self, rank_tools):
        self.rank_tools = rank_tools

    async def rank(self, ctx, page):
        if page.isnumeric() and int(page) < 199:

            page = int(page)

            datas = rank_tools.show_wins(False)
            try: # The lib that i use to create the image throw a error, but for some reason its create the image
                # then a use the try statament to ignore the error
                create_rank_image(datas, page)
            except:
                print('Image Excepted')
            
            await ctx.channel.send(file=File('bot/rank.jpg'))
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


rank_tools = Rank(Sqlite)
rank_commands = RankCommands(rank_tools)

if __name__ == "__main__":    
    pass