import os
import discord
import flask
import waitress
import threading

from dotenv import load_dotenv

from commands.commands import Commands
from exceptions import *
import writer as writer

client = discord.Client()

commands = Commands("$")

@client.event
async def on_message(message):
    try:
        await commands.onMessage(message)
    except InvalidStatementException as e:
        await message.channel.send(embed=writer.printError("Invalid Statement Exception!", e))
    except CommandNotFoundException as e:
        await message.channel.send(embed=writer.printError("Command Not Found Exception!", e))

    #print(message.content)
    
app = flask.Flask(__name__)
    
@app.route("/")
def home():
	return "Bot should be running!"

def run():
    waitress.serve(app, host="127.0.0.1", port="5000")

if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    
    t = threading.Thread(target=run)
    t.start()
    
    print("Bot is online!")
    client.run(token)
