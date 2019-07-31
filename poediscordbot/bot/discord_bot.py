import asyncio
import random
import traceback
from urllib.error import HTTPError

import discord
from discord.ext import commands

import config
from poediscordbot import util
from poediscordbot.bot import pob_output
from poediscordbot.bot import pob_parser
from poediscordbot.util import pastebin, chat_logging, poe_consts
from poediscordbot.util.logging import log

bot = commands.Bot(command_prefix='!', description="x")
bot.remove_command('help')


async def export_dm_logs():
    while not bot.is_closed:
        # log.info("Exporting all DMs. channels: {}".format(len(bot.private_channels)))
        for ch in bot.private_channels:
            recipient = ch.recipients[0]
            if recipient:
                latest_date = chat_logging.get_latest_date_utc(recipient)
                msgs = []
                async for msg in bot.logs_from(ch, after=latest_date):
                    if not msg.author.bot:
                        msgs.append(msg)

                # print("Msgs={}".format(msgs))
                chat_logging.write_to_file(recipient, msgs)

        await asyncio.sleep(config.dm_poll_rate_seconds)  # task runs every x seconds


async def trigger_export_logs():
    await bot.wait_until_ready()
    await export_dm_logs()


if config.dm_auto_log:
    bot.loop.create_task(export_dm_logs())


@bot.event
async def on_ready():
    log.info('Logged in: uname={}, id={}'.format(bot.user.name, bot.user.id))
    if config.presence_message:
        await bot.change_presence(activity=discord.Activity(name=config.presence_message))


@bot.command(pass_context=True)
# @commands.cooldown(1, 5, commands.BucketType.user)
async def pob(ctx, *, key):
    if not config.allow_pming and ctx.message.channel.is_private:
        return
    embed = parse_pob(ctx.message.author, ctx.message.content)
    try:
        if embed:
            await ctx.message.channel.send(embed=embed)
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

    react_to_dms = isinstance(message.channel, discord.abc.PrivateChannel) and config.allow_pming

    # call bot commands, if not a bot command, check the message for pastebins
    # better way to do this would probably be to create the context, then check if its valid, then invoke it. If its valid,its a command, if not, its not. You could backport this to async pretty ez
    # todo: replace async with rewrite of the bot, then use on_command_completion
    if message.author.bot:
        return

    if 'help' in message.content.lower() and react_to_dms:
        await message.channel.send("Paste your pastebin here for a quick overview or use '!pob <pastebin>' for a "
                                   "detailled respoonse.")
        return

    if (react_to_dms or message.channel.name in config.active_channels) \
            and not util.starts_with("!pob", message.content[:4]) \
            and "pastebin.com/" in message.content:
        # check if valid xml
        # send message
        log.debug("A| {}: {}".format(message.channel, message.content))
        try:
            embed = parse_pob(message.author, message.content, minify=True)
            if embed:
                await message.channel.send(embed=embed)
        except HTTPError as err:
            log.error("Pastebin: Invalid pastebin-url msg={}".format(err))
        except pastebin.CaptchaError as err:
            log.error("Pastebin: Marked as spam msg={}".format(err))
            await message.channel.send(err.message)

    else:
        await bot.process_commands(message)


def parse_pob(author, content, minify=False):
    """
    Trigger the parsing of the pastebin link, pass it to the output creating object and send a message back
    :param minify: show minified version of the embed
    :param content: of the message
    :param author: user sending the message
    :return: Embed
    """
    paste_keys = pastebin.fetch_paste_key(content)
    if paste_keys:
        xml = None
        paste_key = random.choice(paste_keys)
        log.info(f"Parsing pastebin with key={paste_key} from author={author}")
        raw_data = pastebin.get_as_xml(paste_key)
        if not raw_data:
            log.error(f"Unable to obtain raw data for pastebin with key {paste_key}")
            return

        xml = pastebin.decode_to_xml(raw_data)
        if not xml:
            log.error(f"Unable to obtain xml data for pastebin with key {paste_key}")
            return

        web_poe_token = util.fetch_xyz_pob_token(raw_data)
        build = pob_parser.parse_build(xml)
        # print(build)
        try:
            embed = pob_output.generate_response(author, build, minified=minify, pastebin_key=paste_key,
                                                 consts=poe_consts, web_poe_token=web_poe_token)
            log.debug(f"embed={embed}; thumbnail={embed.thumbnail}")
            return embed
        except Exception as e:
            log.error("Could not parse pastebin={} - Exception={}".format(paste_key, ''.join(
                traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))))
