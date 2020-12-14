import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('bot-db.db')

    def query(self, sql, commit=False):
        cursor = self.connection.cursor()
        cursor.execute(sql)

        if commit == True:
            self.connection.commit()

        try:
            rows = cursor.fetchall()
            cursor.close()
            return rows
        except:
            cursor.close()

    def queryScript(self, sql, commit=False):
        cursor = self.connection.cursor()
        cursor.executescript(sql)

        if commit == True:
            self.connection.commit()

        try:
            rows = cursor.fetchall()
            cursor.close()
            return rows
        except:
            cursor.close()
        
    def addToRank(self, names_wins_images): # Its not used on bot

        names = names_wins_images['names']

        wins = names_wins_images['wins']

        imgs = names_wins_images['img']


        for name, win, img in zip(names, wins, imgs):
            try:
                self.query(f"insert into rank values ('{name}', '0', '{win}', '{img}', '0')", True)
                print('added', name, win)
            except sqlite3.IntegrityError:
                print('same name', name)

Sqlite = Database()

if __name__ == "__main__":
   pass