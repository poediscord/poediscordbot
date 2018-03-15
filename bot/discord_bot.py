from discord.ext import commands

from util.logging import log
from urllib.error import HTTPError

import discord

import config
import util
from bot.parser import Parser
from bot import pob_output
from util import pastebin

bot = commands.Bot(command_prefix='!', description="descriptinon")


@bot.event
async def on_ready():
    log.info('Logged in: uname={}, id={}'.format(bot.user.name, bot.user.id))
    if config.presence_message:
        await bot.change_presence(game=discord.Game(name=config.presence_message))


@bot.event
async def on_message(message):
    """
    Handle message events
    :param message:
    :return: None
    """
    if message.channel.name in config.active_channels or message.channel.name in config.passive_channels:
        # if the keyword is present in either channel type, display pob message
        if any(util.starts_with(keyword, message.content) for keyword in config.keywords):
            embed = parse_pob(message.author, message.content)
            if embed:
                await bot.send_message(message.channel, embed=embed)
        else:
            # in active channels look for pastebin links
            if message.channel.name in config.active_channels and "pastebin.com/" in message.content:
                # check if valid xml
                # send message
                log.debug("P| {}: {}".format(message.channel, message.content))
                embed = parse_pob(message.author, message.content, minify=True)
                if embed:
                    await bot.send_message(message.channel, embed=embed)


def parse_pob(author, content, minify=False):
    """
    Trigger the parsing of the pastebin link, pass it to the output creating object and send a message back
    :param channel: receiving channel
    :param author: user sending the message
    :param paste_key: pastebin paste key
    :param argument: optional: arguments to determine the output
    :return:
    """
    paste_key = pastebin.fetch_paste_key(content)
    if paste_key:
        xml = None
        log.info("Parsing pastebin with key={}".format(paste_key))

        try:
            xml = pastebin.get_as_xml(paste_key)
        except HTTPError as err:
            log.error("Invalid pastebin-url msg={}".format(err))
        if xml:
            parser = Parser()
            build = parser.parse_build(xml)
            # print(build)

            embed = pob_output.generate_output(author, build) if not minify \
                else pob_output.generate_minified_output(author, build)
            log.debug("embed={}; length={}".format(embed, embed.__sizeof__()))
            return embed
