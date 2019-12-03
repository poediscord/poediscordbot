from instance import config

from poediscordbot.discord_bot import bot
from poediscordbot.util.logging import log

if __name__ == '__main__':

    token = config.token  # create config.py file and enter a new string!
    if token:
        # initialize_logging()

        log.info("Starting pob discord bot...")
        bot.run(token)
    else:
        log.warning("Missing token from config file. Please generate a bot and the token as described: "
                    "https://www.writebots.com/discord-bot-token/")
