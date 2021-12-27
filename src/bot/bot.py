import discord

import bot.writer as writer
import bot.commands.commands as cmds

from exceptions import *

client = discord.Client()

@client.event
async def on_message(message):
    try:
        await commands.on_message(message)
    except InvalidStatementException as e:
        await message.channel.send(embed=writer.print_error(message, "Invalid Statement Exception!", e))
    except CommandNotFoundException as e:
        await message.channel.send(embed=writer.print_error(message, "Command Not Found Exception!", e))
    except CommandErrorException as e:
        await message.channel.send(embed=writer.print_error(message, "Command Error Exception!", e))
    except Exception as e:
        print(e)
        await message.channel.send(embed=writer.print_error(message, "An Unexpected Error Has Occured", "Please Report The Issue!"))

class DiscordBot:
    def __init__(self, invoke_command):
        global commands
        commands = cmds.Commands(invoke_command)
    
    def run(self, token):
        print("Bot is running!")
        client.run(token)