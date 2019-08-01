import random
import traceback

import discord
from discord.ext import commands
from requests import HTTPError

from poediscordbot.bot.cogs.pob import pob_output, util
from poediscordbot.bot.cogs.pob.parser import pob_xml_parser
from poediscordbot.bot.cogs.pob.util import pastebin
from poediscordbot.bot.cogs.pob.build import poe_consts
from poediscordbot.util.logging import log


def setup(bot, active_channels, allow_pming=True):
    bot.add_cog(PathOfBuilding(bot, active_channels, allow_pming))


class PathOfBuilding(commands.Cog):
    def __init__(self, bot, active_channels, allow_pming=True):
        self.bot = bot
        self.active_channels = active_channels
        self.allow_pming = allow_pming

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Handle message events
        :param message: received
        :return: None
        """
        react_to_dms = isinstance(message.channel, discord.abc.PrivateChannel) and self.allow_pming

        if message.author.bot:
            return

        if 'help' in message.content.lower() and react_to_dms:
            await message.channel.send("Paste your pastebin here for a quick overview or use '!pob <pastebin>' for a "
                                       "detailled respoonse.")
            return

        if (react_to_dms or message.channel.name in self.active_channels) \
                and not util.starts_with("!pob", message.content[:4]) \
                and "pastebin.com/" in message.content:
            # check if valid xml
            # send message
            log.debug("A| {}: {}".format(message.channel, message.content))
            try:
                embed = self.__parse_pob(message.author, message.content, minify=True)
                if embed:
                    await message.channel.send(embed=embed)
            except HTTPError as err:
                log.error("Pastebin: Invalid pastebin-url msg={}".format(err))
            except pastebin.CaptchaError as err:
                log.error("Pastebin: Marked as spam msg={}".format(err))
                await message.channel.send(err.message)

    @commands.command(pass_context=True)
    async def pob(self, ctx, *, key):
        if not self.allow_pming and ctx.message.channel.is_private:
            return
        embed = self.__parse_pob(ctx.message.author, ctx.message.content)
        try:
            if embed:
                await ctx.message.channel.send(embed=embed)
        except discord.Forbidden:
            log.info("Tried pasting in channel without access.")

    @staticmethod
    def __parse_pob(author, content, minify=False):
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
            build = pob_xml_parser.parse_build(xml)
            # print(build)
            try:
                embed = pob_output.generate_response(author, build, minified=minify, pastebin_key=paste_key,
                                                     consts=poe_consts, web_poe_token=web_poe_token)
                log.debug(f"embed={embed}; thumbnail={embed.thumbnail}")
                return embed
            except Exception as e:
                log.error("Could not parse pastebin={} - Exception={}".format(paste_key, ''.join(
                    traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))))
