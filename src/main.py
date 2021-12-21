import os
import threading

import dotenv as env

import bot.bot as discordbot
import web.website as website

def run_website():
    port_number = os.getenv("PORT")
    website.run_website(port_number)

def run_discord_bot():
    token = os.getenv("BOT_TOKEN")
    invoke_command = os.getenv("INVOKE_COMMAND")

    discord_bot = discordbot.DiscordBot(invoke_command)
    discord_bot.run(token)

if __name__ == "__main__":
    env.load_dotenv()

    thread = threading.Thread(target=run_website)
    thread.start()
    
    run_discord_bot()
