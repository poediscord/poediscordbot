import asyncio
from urllib.error import HTTPError

import discord
from discord.ext import commands

import config
import util
from bot import pob_output
from bot import pob_parser
from util import pastebin, chat_logging
from util.logging import log

bot = commands.Bot(command_prefix='!', description="x")
bot.remove_command('help')


async def export_dm_logs():
    while not bot.is_closed:

        log.info("Exporting all DMs. channels: {}".format(len(bot.private_channels)))

        for ch in bot.private_channels:
            recipient = ch.recipients[0]
            if recipient:
                latest_date = chat_logging.get_latest_date_utc(recipient)
                msgs=[]
                async for msg in bot.logs_from(ch, after=latest_date):
                    if not msg.author.bot:
                        msgs.append(msg)

                print("Msgs={}".format(msgs))
                chat_logging.write_to_file(recipient, msgs)

        await asyncio.sleep(config.dm_poll_rate_seconds)  # task runs every 60 seconds


async def trigger_export_logs():
    await bot.wait_until_login()
    await export_dm_logs()


if config.dm_auto_log:
    bot.loop.create_task(export_dm_logs())


@bot.event
async def on_ready():
    log.info('Logged in: uname={}, id={}'.format(bot.user.name, bot.user.id))
    if config.presence_message:
        await bot.change_presence(game=discord.Game(name=config.presence_message))


@bot.command(pass_context=True)
# @commands.cooldown(1, 5, commands.BucketType.user)
async def pob(ctx, *, key):
    if not config.allow_pming and ctx.message.channel.is_private:
        return
    embed = parse_pob(ctx.message.author, ctx.message.content)
    try:
        await bot.send_message(ctx.message.channel, embed=embed)
    except discord.Forbidden:
        log.info("Tried pasting in channel without access.")
        # await ctx.say(arg)


@bot.command()
async def export_logs():
    await export_dm_logs()


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
    if message.author.bot:
        return

    if config.allow_pming and message.channel.is_private and 'help' in message.content.lower():
        await bot.send_message(message.channel,
                               "Paste your pastebin here for a quick overview or use '!pob <pastebin>' for a detailled respoonse.")
    if message.channel.name in config.active_channels or (message.channel.is_private and config.allow_pming) \
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
