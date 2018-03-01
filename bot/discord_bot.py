import discord

from bot.pob_output import generate_output
from util import pastebin

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    """
    Handle message events
    :param message:
    :return: None
    """
    print("hello")
    if '!pob https://pastebin.com/' in message.content:
        tmp = await client.send_message(message.channel, "Retrieving POB")
        paste_key = message.content.split('.com/')[1]
        await client.edit_message(tmp, 'POB PasteKey: {}'.format(paste_key))

        if paste_key:
            xml= pastebin.get_as_xml(paste_key)
            print(xml)
            generate_output(xml)
        await client.edit_message(tmp, 'Got Data.')


