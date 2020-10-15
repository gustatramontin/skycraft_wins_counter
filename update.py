import requests
from bs4 import BeautifulSoup

def get_updates():

    URL = 'https://skycraft.com.br/actiong/ranks/load/&gameid=25&type=mg&period=mensal&page=1&order=1&desc=1&vv=1'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    usernames = soup.find_all('td')
    wins = soup.find_all('td', class_='rowsel')

    names_and_wins = {
        "names": [],
        "wins": []
    }

    for name in usernames:
        try:
            names_and_wins["names"].append(name.findChildren('p', recursive=False)[0].text)
        except:
            True

    for win in wins:
        names_and_wins["wins"].append(win.text)

    return names_and_wins


