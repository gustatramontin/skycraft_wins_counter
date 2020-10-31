import requests
from bs4 import BeautifulSoup

import asyncio
import aiohttp

from aiohttp import ClientSession

import nest_asyncio
nest_asyncio.apply()


def get_wins_from_skycraft():

    loop = asyncio.get_event_loop()

    URL = 'https://skycraft.com.br/actiong/ranks/load/&gameid=25&type=mg&period=mensal&page={}&order=1&desc=1&vv=1'

    names_and_wins = {
            "names": [],
            "wins": []
        }
        
    async def request_site(i, session):
        async with session.get(URL.format(i)) as resp:
            text = await resp.read()
        print('requested page', i)

        soup = BeautifulSoup(text.decode('utf-8'), 'html.parser')

        usernames = soup.find_all('td')
        wins = soup.find_all('td', class_='rowsel')

        for name in usernames:
            try:
                names_and_wins["names"].append(name.findChildren('p', recursive=False)[0].text)
            except:
                True

        for win in wins:
            names_and_wins["wins"].append(win.text)

        print('appended page', i)
    
    async def main(i):
        async with ClientSession() as session:
            await request_site(i, session)

        
    loop.run_until_complete(asyncio.gather(*[main(i) for i in range(1,270)]))

    return names_and_wins

if __name__ == "__main__":
    pass

