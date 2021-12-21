import os
import threading

from dotenv import load_dotenv

from bot import DiscordBot
from website import Website

load_dotenv()
    
def run():
    website.run("5000")

if __name__ == "__main__":
    token = os.getenv("BOT_TOKEN")
    invoke_command = os.getenv("INVOKE_COMMAND")
    
    global website
    website = Website(__name__)

    t = threading.Thread(target=run)
    t.start()
    
    discord_bot = DiscordBot(invoke_command)
    discord_bot.run(token)
