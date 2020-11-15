from .db import Sqlite
from .Request import get_wins_from_skycraft

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

        for name in names:
            if name in name_wins["names"]:

                oldSkywins = int(str(skywins[names.index(name)]).replace(',', ''))
                newSkywins = int(name_wins["wins"][name_wins["names"].index(name)].replace(',', ''))
                if newSkywins < oldSkywins:
                    continue

                name_index = names.index(name)
                thisWins = int(wins[name_index])

                self.db.query(f"update rank set wins='{thisWins + (newSkywins-oldSkywins)}', skywins='{newSkywins}' where username='{name}'", True)

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


rank_tools = Rank(Sqlite)

if __name__ == "__main__":    
    pass