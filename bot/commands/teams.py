import discord
from discord import app_commands, ButtonStyle, Button
from bot.utils.teams import create_and_move_teams, move_to_lobby


class TeamButtons(discord.ui.View):
    def __init__(self, interaction: discord.Interaction):
        super().__init__(timeout=None)
        self.interaction = interaction

    @discord.ui.button(label="End Session", style=discord.ButtonStyle.red)
    async def end_session_button(self,interaction:discord.Interaction,button:discord.ui.Button):
        if not self.interaction.user.guild_permissions.move_members:
            await self.interaction.response.send_message("You do not have permission to use this command.")
            return
        
        await interaction.response.edit_message(view=None)
        await move_to_lobby(self.interaction)
        

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
        await interaction.response.send_message(status_msg, view=TeamButtons(interaction))
        return
