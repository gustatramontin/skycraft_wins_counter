from sys import argv
from update import get_updates
from Rank import rank

def update_datas():
    rank.update()

def create_log():
    datas = rank.show_wins(False)
    for data in datas:
        print('User:', data[0], 'Wins:',data[1])

if __name__ == "__main__":
    
    while True:
        
        question = input("Do you want to update(0), print wins(1), break(end)> ")

        if question == '0':
            update_datas()
            continue

        elif question == '1':
            create_log()
            continue

        elif question == 'end':
            break