import requests
from bs4 import BeautifulSoup

def get_updates():

    URL = 'https://skycraft.com.br/actiong/ranks/load/&gameid=25&type=mg&period=mensal&page={}&order=1&desc=1&vv=1'

    names_and_wins = {
            "names": [],
            "wins": []
        }

    for i in range(1, 71):
        page = requests.get(URL.format(i))

        soup = BeautifulSoup(page.content, 'html.parser')

        usernames = soup.find_all('td')
        wins = soup.find_all('td', class_='rowsel')

        for name in usernames:
            try:
                names_and_wins["names"].append(name.findChildren('p', recursive=False)[0].text)
            except:
                True

        for win in wins:
            names_and_wins["wins"].append(win.text)

    return names_and_wins

if __name__ == "__main__":
    pass


