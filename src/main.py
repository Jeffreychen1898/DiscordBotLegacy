import os
import threading

from dotenv import load_dotenv

from bot import DiscordBot
import website as website

load_dotenv()
    
def run_website():
    port_number = os.getenv("PORT")
    website.run(port_number)

def run_discord_bot():
    token = os.getenv("BOT_TOKEN")
    invoke_command = os.getenv("INVOKE_COMMAND")

    discord_bot = DiscordBot(invoke_command)
    discord_bot.run(token)

if __name__ == "__main__":
    thread = threading.Thread(target=run_website)
    thread.start()
    
    run_discord_bot()
