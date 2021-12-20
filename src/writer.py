import discord

def printError(type, message):
    embed = discord.Embed(title="ERROR", color=0xff0000)
    embed.add_field(name=type, value=message, inline=False)
    return embed

def printMessage():
    pass