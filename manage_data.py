from db import Sqlite

class Manage:
    
    def __init__(self, db):
        self.db = db

    def reset(self):
        pass

    def show_wins(self, limit):
        res = self.db.query(f"select username, wins from rank limit {limit}")
        return res

    def recount(self, name_wins):
        result = self.db.query("select username, skywins, wins from rank")

        names = list(map(lambda a: a[0], result))

        skywins = list(map(lambda a: a[1], result))

        wins = list(map(lambda a: a[2], result))

        for name in names:
            if name in name_wins["names"]:
                oldSkywins = int(skywins[names.index(name)])
                newSkywins = int(name_wins["wins"][name_wins["names"].index(name)].replace(',', ''))
                thisWins = int(wins[name_wins["names"].index(name)])

                self.db.query(f"update rank set wins='{thisWins + (newSkywins-oldSkywins)}', skywins='{newSkywins}' where username='{name}'", True)


manage = Manage(Sqlite)

if __name__ == "__main__":    
    manage.recount({
        "names": ['test'],
        "wins": [1007]
    })



