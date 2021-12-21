import discord

import writer as writer
from commands.commands import Commands
from exceptions import *

client = discord.Client()

@client.event
async def on_message(message):
    try:
        await commands.on_message(message)
    except InvalidStatementException as e:
        await message.channel.send(embed=writer.printError("Invalid Statement Exception!", e))
    except CommandNotFoundException as e:
        await message.channel.send(embed=writer.printError("Command Not Found Exception!", e))

class DiscordBot:
    def __init__(self, invoke_command):
        global commands
        commands = Commands(invoke_command)
    
    def run(self, token):
        print("Bot is running!")
        client.run(token)