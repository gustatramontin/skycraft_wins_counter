from discord import Embed

def create_embed(title=' ', description=' ', color=0xff1a1a, fild_name=' ', fild_value=' '):
    embed = Embed(title=title, description=description, color=color)

    embed.add_field(name=fild_name, value=fild_value)

    return embed