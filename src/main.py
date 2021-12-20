import os
import discord

from dotenv import load_dotenv

from commands import *
from exceptions import *

client = discord.Client()

commands = Commands("!")

def printError(type, message):
    embed = discord.Embed(title="ERROR", color=0xff0000)
    embed.add_field(name=type, value=message, inline=False)
    return embed

@client.event
async def on_message(message):
    try:
        commands.onMessage(message)
    except InvalidStatementException as e:
        await message.channel.send(embed=printError("Invalid Statement Exception!", e))
    except CommandNotFoundException as e:
        await message.channel.send(embed=printError("Command Not Found Exception!", e))

    #print(message.content)

if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    client.run(token)
