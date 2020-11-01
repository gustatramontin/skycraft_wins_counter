import matplotlib.pyplot as plt
from .Rank import rank_tools
from discord import File

class RankChart: # ITS NOT WORKIN PROPORLY

    def __init__(self, channel):
        self.channel = channel # discord channel to show the charts

    def get_wins(self):
        data = rank_tools.show_wins(10)
        return data

    async def diplay(self):
        await self.delete()
        wins_and_names =self.get_wins()
        names = []
        wins = []
        labels = []

        for name, win in wins_and_names:
            names.append(name)
            wins.append(win)
            labels.append(f"{name}({win})")

        plt.pie(wins, labels=labels)
        plt.savefig("chart.png")
        plt.close()

        image = File("chart.png")

        await self.channel.send(file=image)


    async def delete(self):
        try:
            messages = await self.channel.history().flatten()
            for message in messages: 
                await message.delete()
        except:
            print('No laste message')
 