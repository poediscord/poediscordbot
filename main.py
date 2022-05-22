from instance import config

from poediscordbot.discord_bot import bot
from poediscordbot.util.logging import log

if __name__ == '__main__':

    token = config.token
    if token and token != 'supersecrettoken':
        log.info("Starting pob discord bot...")
        bot.run(token)
    else:
        log.warning(f"Missing token or default token in config file. Please generate a bot and the token as described: "
                    "https://www.writebots.com/discord-bot-token/")
