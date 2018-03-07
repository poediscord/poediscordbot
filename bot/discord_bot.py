import logging
from urllib.error import HTTPError

import discord

import config
from bot.parser import Parser
from bot import pob_output
from util import pastebin

client = discord.Client()


@client.event
async def on_ready():
    logging.info('Logged in: uname={}, id={}'.format(client.user.name, client.user.id))


@client.event
async def on_message(message):
    """
    Handle message events
    :param message:
    :return: None
    """
    if message.channel.name in config.active_channels and "pastebin.com/" in message.content:
        # check if valid xml
        # send message
        logging.info("P| {}: {}".format(message.channel, message.content))
        embed = parse_pob(message,minify=True)
        if embed:
            await client.send_message(message.channel, embed=embed)

    if message.channel.name in config.passive_channels:
        logging.info("A| {}: {} [keywords={}]".format(message.channel, message.content,
                                                      config.keywords))
        if any(keyword in message.content for keyword in config.keywords):
            embed = parse_pob(message)
            if embed:
                await client.send_message(message.channel, embed=embed)


def parse_pob(message, minify=False):
    """
    Trigger the parsing of the pastebin link, pass it to the output creating object and send a message back
    :param channel: receiving channel
    :param author: user sending the message
    :param paste_key: pastebin paste key
    :param argument: optional: arguments to determine the output
    :return:
    """
    paste_key = pastebin.fetch_paste_key(message.content)
    if paste_key:
        xml = None
        try:
            xml = pastebin.get_as_xml(paste_key)
        except HTTPError as err:
            logging.info("Invalid url msg={}".format(err))
        if xml:
            parser = Parser()
            build = parser.parse_build(xml)

            embed = pob_output.generate_output(message.author, build) if not minify \
                else pob_output.generate_minified_output(message.author,build)
            logging.info("sending reply to channel: {}".format(message.channel))
            logging.info("embed={}; length={}".format(embed, embed.__sizeof__()))
            return embed
