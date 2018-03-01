import discord
from discord import Embed

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
    print(message.content)
    if '!pob' in message.content and 'pastebin.com/' in message.content:
        tmp = await client.send_message(message.channel, "Retrieving POB")
        paste_key = message.content.split('.com/')[1]
        await client.edit_message(tmp, 'POB PasteKey: {}'.format(paste_key))

        if paste_key:
            xml= pastebin.get_as_xml(paste_key)
            # data=generate_output(xml)
            embed = Embed(title='PoB Discord', color=0x0433ff)
            embed.set_thumbnail(url='https: // docs.python.org / 2 / _static / py.png')
            embed.add_field(name='test', value='https: // docs.python.org / 2 / _static / py.png', inline = False)
            embed.add_field(name='test2', value='```dd```')
            await client.edit_message(tmp,embed=embed)


