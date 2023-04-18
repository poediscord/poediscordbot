import discord
from discord import app_commands
from discord.ext import commands

from poediscordbot.util.logging import log


def setup(bot):
    bot.add_cog(SyncCog(bot))


class SyncCog(commands.Cog):
    def __init__(self, pobBot):
        self.pobBot = pobBot
        log.info("Sync cog loaded")

    @app_commands.command(name="sync-cmds", description="Update the command tree")
    async def sync_cmds(self, interaction: discord.Interaction) -> None:
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You are not authorized to run this command.", ephemeral=True)
        else:
            log.info("Trying to sync command tree globally")
            await interaction.response.defer(ephemeral=True)
            await interaction.followup.send("Syncing the bot's tree...", ephemeral=True)
            cmds = await self.pobBot.tree.sync()
            command_names = self.pobBot.get_command_names(cmds)
            log.info(f"commands [{command_names}] from tree synced")
            await interaction.followup.send(f"commands [{command_names}] from tree synced", ephemeral=True)
