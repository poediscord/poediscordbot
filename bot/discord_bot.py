import logging

import discord
from discord import Embed

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
    print(message.content)
    if '!pob' in message.content and 'pastebin.com/' in message.content:
        tmp = await client.send_message(message.channel, "Retrieving POB")
        paste_key = message.content.split('.com/')[1]
        await client.edit_message(tmp, 'POB PasteKey: {}'.format(paste_key))

        if paste_key:
            xml= pastebin.get_as_xml(paste_key)
            embed=generate_output(xml)

            await client.edit_message(tmp,embed=embed)


