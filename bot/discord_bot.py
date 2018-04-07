from urllib.error import HTTPError

import discord
from discord.ext import commands

import config
import util
from bot import pob_output
from bot import pob_parser
from util import pastebin
from util.logging import log

bot = commands.Bot(command_prefix='!', description="x")
bot.remove_command('help')


@bot.event
async def on_ready():
    log.info('Logged in: uname={}, id={}'.format(bot.user.name, bot.user.id))
    if config.presence_message:
        await bot.change_presence(game=discord.Game(name=config.presence_message))


@bot.command(pass_context=True)
# @commands.cooldown(1, 5, commands.BucketType.user)
async def pob(ctx, *, key):
    embed = parse_pob(ctx.message.author, ctx.message.content)
    try:
        await bot.send_message(ctx.message.channel, embed=embed)
    except discord.Forbidden:
        log.info("Tried pasting in channel without access.")
    # await ctx.say(arg)


@bot.event
async def on_message(message):
    """
    Handle message events
    :param message:
    :return: None
    """
    # call bot commands, if not a bot command, check the message for pastebins
    # better way to do this would probably be to create the context, then check if its valid, then invoke it. If its valid,its a command, if not, its not. You could backport this to async pretty ez

    # todo: replace async with rewrite of the bot, then use on_command_completion
    if message.channel.name in config.active_channels \
            and not util.starts_with("!pob", message.content[:4]) \
            and "pastebin.com/" in message.content:
        # check if valid xml
        # send message
        log.debug("A| {}: {}".format(message.channel, message.content))
        embed = parse_pob(message.author, message.content, minify=True)
        if embed:
            await bot.send_message(message.channel, embed=embed)
    else:
        await bot.process_commands(message)


def parse_pob(author, content, minify=False):
    """
    Trigger the parsing of the pastebin link, pass it to the output creating object and send a message back
    :param channel: receiving channel
    :param author: user sending the message
    :param paste_key: pastebin paste key
    :param argument: optional: arguments to determine the output
    :return: Embed
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
            build = pob_parser.parse_build(xml)
            # print(build)

            embed = pob_output.generate_response(author, build, minified=minify)

            log.debug("embed={}; thumbnail={}; length={}".format(embed, embed.thumbnail, embed.__sizeof__()))
            return embed
