import discord
from discord import app_commands, utils
from bot.utils.teams import create_and_move_teams, move_to_lobby
from bot.utils.translations import translate


class TeamButtons(discord.ui.View):
    """
    A custom UI view for handling the "End Session" button
    """
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label=translate("commands.teams.end_button"), style=discord.ButtonStyle.red)
    async def end_session_button(self,interaction:discord.Interaction,button:discord.ui.Button):
        if not interaction.user.guild_permissions.move_members:
            await interaction.response.send_message(translate("commands.teams.permission_error"))
            return
        
        await interaction.response.edit_message(view=None)
        await move_to_lobby(interaction)
        

def setup_team_commands(tree: app_commands.CommandTree, guild):
    """
    This function registers the /teams command and its associated functionality. It ensures that the command
    is only executable by users with administrator permissions in the CS2 voice channel. When executed, it creates
    teams and moves users into them.

    Args:
        tree (app_commands.CommandTree): The command tree to register the command to.
        guild: The guild to associate the command with.
    """
    
    @tree.command(description=translate("commands.teams.description"))
    async def teams(interaction: discord.Interaction):
        cs2_channel = utils.get(interaction.guild.voice_channels, name='CS2')

        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(translate("commands.teams.permission_error"), ephemeral=True)
            return
        
        if interaction.channel.id != cs2_channel.id:
            await interaction.response.send_message(translate("commands.teams.wrong_channel"), ephemeral=True)
            return

        if interaction.user.voice is None or interaction.user.voice.channel.name != 'CS2':
            await interaction.response.send_message(translate("commands.teams.not_in_channel"), ephemeral=True)
            return

        if cs2_channel:
            if len(cs2_channel.members) < 2:
                await interaction.response.send_message(translate("commands.teams.not_enough"), ephemeral=True)
                return
        else:
            await interaction.response.send_message("[ERROR] CS2 Channel not found!", ephemeral=True)
            return
        
        await interaction.response.send_message(translate("commands.teams.creating_teams"), ephemeral=True)
        
        # Create and move teams
        msg = await create_and_move_teams(interaction)
        if type(msg) == str:
            await interaction.followup.send(msg, view=TeamButtons())
        else:
            await interaction.followup.send(embed=msg, view=TeamButtons())
