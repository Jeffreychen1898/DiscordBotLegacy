import os
import discord

from dotenv import load_dotenv

from commands.commands import Commands
from exceptions import *
import writer as writer

client = discord.Client()

commands = Commands("!")

@client.event
async def on_message(message):
    try:
        await commands.onMessage(message)
    except InvalidStatementException as e:
        await message.channel.send(embed=writer.printError("Invalid Statement Exception!", e))
    except CommandNotFoundException as e:
        await message.channel.send(embed=writer.printError("Command Not Found Exception!", e))

    #print(message.content)

if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    client.run(token)

    print("Bot is online!")
