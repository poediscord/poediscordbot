import random
from datetime import datetime
from pathlib import Path

import discord
from discord import app_commands, Embed
from discord.ext import commands, tasks
from instance import config
from requests import HTTPError

from poediscordbot.cogs.pob import util
from poediscordbot.cogs.pob.importers import pastebin, pob_xml_decoder, PasteData
from poediscordbot.cogs.pob.importers.pastebin import PastebinImporter
from poediscordbot.cogs.pob.importers.pobbin import PobBinImporter
from poediscordbot.cogs.pob.importers.poeninja import PoeNinjaImporter
from poediscordbot.cogs.pob.output import pob_output
from poediscordbot.cogs.pob.poe_data import poe_consts
from poediscordbot.cogs.pob.util.treerenderer import TreeRenderer
from poediscordbot.pob_xml_parser import pob_xml_parser
from poediscordbot.util.logging import log


def setup(bot, active_channels, allow_pming=True):
    bot.add_cog(PoBCog(bot, active_channels, allow_pming))


class PoBCog(commands.Cog):
    def __init__(self, bot, active_channels, allow_pming=True):
        self.bot = bot
        self.active_channels = active_channels
        self.allow_pming = allow_pming
        self.__root_dir, self.__enable_tree_renderer, self.__tree_renderer_deletion_threshold_minutes, \
        self.__tree_img_dir = self.read_conf()
        log.info("Pob cog loaded")
        if self.__enable_tree_renderer:
            self.renderer = TreeRenderer(self.__root_dir + 'resources/tree_3_20.min.json')
            self.cleanup_imgs.start()

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
                xml, paste_data = self._fetch_xml(message.author, message.content)
                if xml:
                    embed, file = self._generate_embed(paste_data, xml, message.author, minify=True)
                    if embed:
                        await message.channel.send(embed=embed, file=file)
            except HTTPError as err:
                log.error(f"Pastebin: Invalid pastebin-url msg={err}")
            except pastebin.CaptchaError as err:
                log.error(f"Pastebin: Marked as spam msg={err}")
                await message.channel.send(err.message)

    @tasks.loop(minutes=config.tree_image_cleanup_minute_cycle)
    async def cleanup_imgs(self):
        path = Path(self.__tree_img_dir)
        log.info(f"Cleaning up image dir '{path}'")
        self.make_tmp_dir()
        try:
            for file in path.iterdir():
                creation_time = file.stat().st_ctime
                if creation_time and creation_time > 0:
                    created = datetime.fromtimestamp(creation_time)
                    log.info(f"checking {file}: created: {created.isoformat()}")
                    delta = datetime.now() - created
                    deletable = delta.seconds > self.__tree_renderer_deletion_threshold_minutes
                    if file.is_file() and deletable:
                        file.unlink(missing_ok=True)
                        log.info(f"Deleted {file}")
        except Exception as e:
            log.error(e)

    @app_commands.command(name="deathbeams-pobs", description="Give me the spice")
    async def deathbeams_pobs(self, interaction: discord.Interaction) -> None:
        embed = Embed(title='What is deathbeam up to now?', url="https://pobb.in/u/thedeathbeam", color=config.color)
        embed.set_image(
            url="https://raw.githubusercontent.com/poediscord/poediscordbot/master/resources/img/surprise.png")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="pob", description="Paste your pastebin, pobbin or poe.ninja pastes here")
    async def pob(self, interaction: discord.Interaction, paste_url: str) -> None:
        log.info(f"{interaction.user} called pob with url={paste_url}")
        await interaction.response.defer(ephemeral=True)
        # first followup ignores ephemeral, still set to true if this changes -> further followups can change it
        await interaction.followup.send(f"Parsing your pob paste now...", ephemeral=True)

        if not self.allow_pming and interaction.message.channel.is_private:
            return
        xml, paste_key = self._fetch_xml(interaction.user, paste_url)
        if xml:
            embed, file = self._generate_embed(paste_key, xml, interaction.user)
            try:
                if embed and file:
                    await interaction.followup.send(f"parsing result for url: {paste_url}", ephemeral=False,
                                                    embed=embed, file=file)
                elif embed:
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

    def _generate_embed(self, paste_data: PasteData, xml, author, minify=False) -> (Embed, discord.File):
        if xml:
            build = pob_xml_parser.parse_build(xml)
            try:
                embed = pob_output.generate_response(author, build, minified=minify, paste_data=paste_data,
                                                     non_dps_skills=poe_consts)
                file = None
                if self.__enable_tree_renderer:
                    path = Path(self.__tree_img_dir)
                    path.mkdir(exist_ok=True, parents=True)
                    expected_filename = f"{path}/{paste_data.source_site}_{paste_data.key}.png"
                    if expected_filename and not Path(expected_filename).exists():
                        svg = self.renderer.parse_tree(build.tree_nodes,
                                                       file_name=f"{path}/{paste_data.source_site}_{paste_data.key}.svg",
                                                       render_size=1500)
                        self.renderer.to_png(svg, f"{path}/{paste_data.source_site}_{paste_data.key}.png")
                    file = discord.File(f"{path}/{paste_data.source_site}_{paste_data.key}.png", filename="tree.png")
                    embed.set_image(url=f"attachment://tree.png")

                log.debug(f"embed={embed}; thumbnail={embed.thumbnail}")
                return embed, file
            except Exception as e:
                log.error(f"Could not parse build from {paste_data.source_url} - Exception={e}")

    def make_tmp_dir(self):
        path = Path(self.__root_dir) / "tmp/img"
        path.mkdir(exist_ok=True, parents=True)
        return path

    def read_conf(self):
        return config.ROOT_DIR, config.render_tree_image, config.tree_image_delete_threshold_seconds, config.tree_image_dir
