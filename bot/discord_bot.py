import logging
from asyncio import sleep

import discord

from bot.parser import Parser
from bot.pob_output import generate_output
from config import channels
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
    if '!pob' in message.content and 'pastebin.com/' in message.content:
        # tmp = await client.send_message(message.channel, "Retrieving POB")
        paste_key = message.content.split('.com/')[1]
        # await client.edit_message(tmp, 'POB PasteKey: {}'.format(paste_key))
        if message.channel.name in channels:
            if paste_key:
                xml = pastebin.get_as_xml(paste_key)
                parser = Parser()
                build = parser.parse_build(xml)
                embed = generate_output(message.author, build)
                logging.info("sending reply to channel: {}".format(message.channel))
                logging.info("embed={}; length={}".format(embed,embed.__sizeof__()))
                try:
                    await client.send_message(message.channel, embed=embed)
                except discord.HTTPException as exception:
                    logging.error("HTTP Exception: {}".format(exception.response.text))

                # await client.send_message(message.channel, embed=embed)
