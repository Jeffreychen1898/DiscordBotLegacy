import os
import discord

from dotenv import load_dotenv

#from commands import *
import commands.commands as cmd
import exceptions
import writer

client = discord.Client()

commands = cmd.Commands("!")

@client.event
async def on_message(message):
    try:
        await commands.onMessage(message)
    except exceptions.InvalidStatementException as e:
        await message.channel.send(embed=writer.printError("Invalid Statement Exception!", e))
    except exceptions.CommandNotFoundException as e:
        await message.channel.send(embed=writer.printError("Command Not Found Exception!", e))

    #print(message.content)

if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    client.run(token)
