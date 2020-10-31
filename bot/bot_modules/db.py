import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('../bot-db.db')

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
        
    def addToRank(self, names, wins):
        for name, win in zip(names, wins):
            try:
                self.query(f"insert into rank values ('{name}', '0', '{win}')", True)
                print('added', name, win)
            except sqlite3.IntegrityError:
                print('same name', name)

Sqlite = Database()

if __name__ == "__main__":
   pass