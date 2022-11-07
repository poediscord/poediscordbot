import random
import traceback

import discord
from discord import app_commands
from discord.ext import commands
from requests import HTTPError

from poediscordbot.cogs.pob import util
from poediscordbot.cogs.pob.importers import pastebin, pob_xml_decoder, PasteData
from poediscordbot.cogs.pob.importers.pastebin import PastebinImporter
from poediscordbot.cogs.pob.importers.pobbin import PobBinImporter
from poediscordbot.cogs.pob.importers.poeninja import PoeNinjaImporter
from poediscordbot.cogs.pob.output import pob_output
from poediscordbot.cogs.pob.poe_data import poe_consts
from poediscordbot.pob_xml_parser import pob_xml_parser
from poediscordbot.util.logging import log


def setup(bot, active_channels, allow_pming=True):
    bot.add_cog(PoBCog(bot, active_channels, allow_pming))


class PoBCog(commands.Cog):
    def __init__(self, bot, active_channels, allow_pming=True):
        self.bot = bot
        self.active_channels = active_channels
        self.allow_pming = allow_pming
        log.info("Pob cog loaded")

    @staticmethod
    def _contains_supported_url(content):
        """
        Filter message content for supported urls
        :param content: message content
        :return: true if any supported site is found
        """
        return "https://pobb.in/" in content or "https://pastebin.com/" in content or "https://poe.ninja/pob" in content

    def in_allowed_channel(self, channel):
        return channel.id in self.active_channels or (channel.parent and channel.parent.id in self.active_channels)

    @commands.Cog.listener(name="on_message")
    async def paste_message_parser(self, message: discord.Message):
        """
        Handle message events
        :param message: received
        :return: None
        """
        react_to_dms = isinstance(message.channel, discord.abc.PrivateChannel) and self.allow_pming

        if message.author.bot:
            return

        if 'help' in message.content.lower() and react_to_dms:
            await message.channel.send("Paste your pastebin here for a quick overview or use /pob <pastebin>' for a "
                                       "detailed response.")
            return

        if react_to_dms or self.in_allowed_channel(message.channel) \
                and not util.starts_with("!pob", message.content[:4]) \
                and self._contains_supported_url(message.content):
            # check if valid xml
            # send message
            log.debug(f"A| {message.channel}: {message.content}")
            try:
                xml, paste_key = self._fetch_xml(message.author, message.content)
                if xml:
                    embed = self._generate_embed(xml, message.author, paste_key, minify=True)
                    if embed:
                        await message.channel.send(embed=embed)
            except HTTPError as err:
                log.error(f"Pastebin: Invalid pastebin-url msg={err}")
            except pastebin.CaptchaError as err:
                log.error(f"Pastebin: Marked as spam msg={err}")
                await message.channel.send(err.message)

    @app_commands.command(name="pob", description="Paste your pastebin, pobbin or poe.ninja pastes here")
    async def pob(self, interaction: discord.Interaction, paste_url: str) -> None:
        log.info(f"{interaction.user} called pob with url={paste_url}")
        await interaction.response.defer(ephemeral=True)
        # first followup ignores ephemeral, still set to true if this changes -> further followups can change it
        await interaction.followup.send(f"Parsing your pastebin now...", ephemeral=True)

        if not self.allow_pming and interaction.message.channel.is_private:
            return
        xml, paste_key = self._fetch_xml(interaction.user, paste_url)
        if xml:
            embed = self._generate_embed(xml, interaction.user, paste_key)
            try:
                if embed:
                    await interaction.followup.send(f"parsing result for url: {paste_url}", ephemeral=False,
                                                    embed=embed)
                else:
                    await interaction.followup.send(f"Unable to parse pob from url: {paste_url}", ephemeral=True)
            except discord.Forbidden:
                log.info("Tried pasting in channel without access.")
        else:
            await interaction.followup.send(f"Unable to parse pob from url: {paste_url}", ephemeral=True)

    @staticmethod
    def _fetch_xml(author, content) -> (str, str, PasteData):
        """
        Trigger the parsing of the pastebin link, pass it to the output creating object and send a message back
        :param minify: show minified version of the embed
        :param content: of the message
        :param author: user sending the message
        :return: Embed
        """
        importer = None
        source_site = None
        if 'pastebin.com' in content:
            importer = PastebinImporter(content)
            source_site = 'pastebin'
        if 'pobb.in' in content:
            importer = PobBinImporter(content)
            source_site = 'pobbin'
        if 'poe.ninja' in content:
            importer = PoeNinjaImporter(content)
            source_site = 'poeninja'

        if importer and importer.keys:
            paste_key = random.choice(importer.keys)
            log.info(f"Parsing pob from {author} for key={paste_key}, using {importer.__class__}")
            raw_data = importer.fetch_data(paste_key)
            if not raw_data:
                log.error(f"Unable to obtain raw data for pastebin with key {paste_key}")
                return None, None, None

            xml = pob_xml_decoder.decode_to_xml(raw_data)
            if not xml:
                log.error(f"Unable to obtain xml data for pastebin with key {paste_key}")
                return None, None, None
            return xml, PasteData(paste_key, importer.get_source_url(paste_key), source_site)
        else:
            log.error(f"No Paste key found")
            return None, None, None

    @staticmethod
    def _generate_embed(xml, author, paste_data: PasteData, minify=False):
        if xml:
            build = pob_xml_parser.parse_build(xml)
            try:
                embed = pob_output.generate_response(author, build, minified=minify, paste_data=paste_data,
                                                     non_dps_skills=poe_consts)
                log.debug(f"embed={embed}; thumbnail={embed.thumbnail}")
                return embed
            except Exception as e:
                ex_msg = ''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))
                log.error(f"Could not parse build from {paste_data.source_url} - Exception={ex_msg}")
