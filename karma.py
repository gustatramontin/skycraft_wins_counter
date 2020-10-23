from db import Sqlite
from datetime import datetime

def add_member(username):
    time = str(datetime.now())[:10]
    print(f'Name: {username}, time: {time}')
    try:
        Sqlite.query(f"insert into karma values ('{username}', '0', '{time}')", True)
    except:
        print('Exists')

def get_karma_data():
    users_data = Sqlite.query('select * from karma order by karma desc')

    return users_data

def get_karma_by_name(name):
    try:
        karma = Sqlite.query(f"select karma from karma where username='{name}'")[0][0]
    except:
        karma = None
    return karma

def check_date(old_date):

    new_date = str(datetime.now())[:10]

    if int(old_date[8:10])+2 <= int(new_date[8:10]) or int(new_date[5:7]) > int(old_date[5:7]) or int(new_date[:4]) > int(old_date[:4]):
        return True
    else:
        return False

def add_karma(name, sign, author):
    if sign == '+':
        current_karma = int(Sqlite.query(f"select karma from karma where username='{name}'")[0][0])+1
    else:
        current_karma = int(Sqlite.query(f"select karma from karma where username='{name}'")[0][0])-1
    current_time = str(datetime.now())[:10]

    print(current_karma)

    Sqlite.query(f"update karma set karma='{current_karma}', time='{current_time}' where username='{author}'", True)

