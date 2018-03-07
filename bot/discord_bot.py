import logging
from asyncio import sleep

import discord

import config
from bot.parser import Parser
from bot.pob_output import generate_output
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
    if message.channel.name in config.active_channels:
        # check if valid xml
        # send message
        logging.info("P| {}: {}".format(message.channel, message.content))
        paste_key = message.content.split('pastebin.com/')[1]
        await parse_pob(message.channel, message.author, paste_key)

    if message.channel.name in config.passive_channels:
        logging.info("A| {}: {} [keywords={}, present={}]".format(message.channel, message.content,
                                                           config.keywords, any(keyword in message.content for keyword in config.keywords)))

        if any(keyword in message.content for keyword in config.keywords):
            # '!pob' in message.content and 'pastebin.com/' in message.content:
            paste_key = message.content.split('pastebin.com/')[1]
            await parse_pob(message.channel, message.author, paste_key)


async def parse_pob(channel, author, paste_key, argument=None):
    """
    Trigger the parsing of the pastebin link, pass it to the output creating object and send a message back
    :param channel: receiving channel
    :param author: user sending the message
    :param paste_key: pastebin paste key
    :param argument: optional: arguments to determine the output
    :return:
    """
    if paste_key:
        xml = pastebin.get_as_xml(paste_key)
        if xml:
            parser = Parser()
            build = parser.parse_build(xml)

            embed = generate_output(author, build)
            logging.info("sending reply to channel: {}".format(channel))
            logging.info("embed={}; length={}".format(embed, embed.__sizeof__()))
            try:
                await client.send_message(channel, embed=embed)
            except discord.HTTPException as exception:
                logging.error("HTTP Exception: {}".format(exception.response.text))

