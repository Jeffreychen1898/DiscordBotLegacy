import os
import discord
import flask
import waitress
import threading

from dotenv import load_dotenv

from bot import DiscordBot

load_dotenv()
    
app = flask.Flask(__name__)
    
@app.route("/")
def home():
	return "Bot should be running!"

def run():
    print("Website is online!")
    waitress.serve(app, port="5000")

if __name__ == "__main__":
    token = os.getenv("BOT_TOKEN")
    invoke_command = os.getenv("INVOKE_COMMAND")
    
    t = threading.Thread(target=run)
    t.start()
    
    discord_bot = DiscordBot(invoke_command)
    discord_bot.run(token)
