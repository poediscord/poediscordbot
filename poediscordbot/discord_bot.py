import asyncio

import discord
from discord.ext import commands
from instance import config

from poediscordbot.cogs.pob.pob_cog import PoBCog
from poediscordbot.util import chat_logging
from poediscordbot.util.logging import log

bot = commands.Bot(command_prefix='!', description="x", max_messages=101, guild_subscriptions=False, fetch_offline_members=False)
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
    bot.add_cog(PoBCog(bot, config.active_channels, config.allow_pming))
    log.info(f'Logged in: uname={bot.user.name}, id={bot.user.id}')
    if config.presence_message:
        await bot.change_presence(activity=discord.Activity(name=config.presence_message))


@bot.command()
async def export_logs():
    await export_dm_logs()
