import config
from src.bot.discord_bot import bot
from src.util.logging import log

if __name__ == '__main__':
    token = config.token  # create config.py file and enter a new string!
    if token:
        # initialize_logging()

        log.info("Starting pob discord bot...")
        bot.run(token)
