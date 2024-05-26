from discord import app_commands

# Import the command setup functions
from bot.commands.teams import setup_team_commands
from bot.commands.maps import setup_map_commands
from bot.commands.stats import setup_stats_commands
from bot.commands.play import setup_play_commands
from bot.commands.vac_check import setup_vac_check_commands

def setup_commands(tree: app_commands.CommandTree, guild):
    """
    Set up all bot commands for the given guild.

    This function initializes the bot's commands by calling the setup functions
    for each command category: teams, maps, stats, and play notifications.

    Parameters:
    - tree (app_commands.CommandTree): The command tree to which the commands will be added.
    - guild (discord.Guild): The guild for which the commands are being set up.

    Usage:
        setup_commands(tree, guild)
    """
    setup_team_commands(tree, guild)
    setup_map_commands(tree, guild)
    setup_stats_commands(tree, guild)
    setup_play_commands(tree, guild)
    setup_vac_check_commands(tree, guild)