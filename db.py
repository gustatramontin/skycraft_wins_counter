import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('rank.db')

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
            self.query(f"insert into rank values ('{name}', '0', '{win}')", True)

Sqlite = Database()

if __name__ == "__main__":
    Sqlite.query("update rank set wins=1 where username='test'", True)