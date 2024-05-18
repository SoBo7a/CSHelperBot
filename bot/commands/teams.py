import discord
from discord import app_commands, utils
from bot.utils.teams import create_and_move_teams, move_to_lobby


class TeamButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="End Session", style=discord.ButtonStyle.red)
    async def end_session_button(self,interaction:discord.Interaction,button:discord.ui.Button):
        if not interaction.user.guild_permissions.move_members:
            await interaction.response.send_message("You do not have permission to use this command.")
            return
        
        await interaction.response.edit_message(view=None)
        await move_to_lobby(interaction)
        

def setup_team_commands(tree: app_commands.CommandTree, guild):
    
    @tree.command(description="Creates and moves Users to Teams.")
    async def teams(interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.")
            return

        if interaction.user.voice is None or interaction.user.voice.channel.name != 'CS2':
            await interaction.response.send_message("You need to be in the 'CS2' voice channel to use this command.")
            return

        cs2_channel = utils.get(interaction.guild.voice_channels, name='CS2')
        if cs2_channel:
            if len(cs2_channel.members) < 2:
                await interaction.response.send_message("There are not enough members in the CS2 channel to create teams.")
                return
        else:
            await interaction.response.send_message("[ERROR] CS2 Channel not found!")
            return
        
        msg = await create_and_move_teams(interaction)
        if type(msg) == str:
            await interaction.response.send_message(msg, view=TeamButtons())
        else:
            await interaction.response.send_message(embed=msg, view=TeamButtons())
        return
