from os import system
import json
from interface import update
from manage_data import manage

update()

datas = manage.show_wins(20)

json_var = {
    "name": [],
    "wins": []
}

for data in datas:
    json_var['name'].append(data[0])
    json_var['wins'].append(data[1])

#print(json.dumps(json_var))

print('test')
