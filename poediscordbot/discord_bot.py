import discord
from discord.ext import commands
from discord.ext.commands import bot
from instance import config

from poediscordbot.cogs.pob.pob_cog import PoBCog
from poediscordbot.util.logging import log


class PobBot(commands.Bot):
    def __init__(self, command_prefix):
        intents = discord.Intents(message_content=True, messages=True, guilds=True, dm_messages=True)
        commands.Bot.__init__(self, command_prefix=command_prefix, self_bot=False, intents=intents)
        self.owner_ids = config.owners
        self.remove_command('help')

    async def on_ready(self):
        await self.add_cog(PoBCog(bot, config.active_channels, config.allow_pming))
        log.info(f'Logged in: uname={self.user.name}, id={self.user.id}')
        if config.presence_message:
            await self.change_presence(activity=discord.Activity(name=config.presence_message))
        log.info("Trying to sync command tree globally")
        await self.tree.sync()
        log.info("Command tree synced")
