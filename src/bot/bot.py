import discord

import bot.writer as writer
import bot.commands.commands as cmds

from exceptions import *

intents = discord.Intents.default()
intents.members = True
writer.client = discord.Client(intents=intents)

@writer.client.event
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
        await message.channel.send(embed=writer.print_error(message, "An Unexpected Error Has Occured", "Please Report The Issue!"))
        raise e

class DiscordBot:
    def __init__(self, invoke_command):
        global commands
        commands = cmds.Commands(invoke_command)
    
    def run(self, token):
        print("Bot is running!")
        writer.client.run(token)