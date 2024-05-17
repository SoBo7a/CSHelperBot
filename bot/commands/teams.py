import discord
from discord import app_commands
from bot.utils.teams import create_and_move_teams, move_to_lobby

def setup_team_commands(tree: app_commands.CommandTree, guild):
    @tree.command()
    async def teams(interaction: discord.Interaction):
        """Creates and moves users to teams."""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.")
            return

        if interaction.user.voice is None or interaction.user.voice.channel.name != 'CS2':
            await interaction.response.send_message("You need to be in the 'CS2' voice channel to use this command.")
            return

        status_msg = await create_and_move_teams(interaction)
        await interaction.response.send_message(status_msg)
        return

    @tree.command()
    async def back(interaction: discord.Interaction):
        """Moves all users back to the CS2 channel."""
        if not interaction.user.guild_permissions.move_members:
            await interaction.response.send_message("You do not have permission to use this command.")
            return

        await move_to_lobby(interaction)
