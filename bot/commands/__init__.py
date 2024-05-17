from discord import app_commands

# Import the command setup functions
from bot.commands.teams import setup_team_commands
from bot.commands.maps import setup_map_commands

def setup_commands(tree: app_commands.CommandTree, guild):
    setup_team_commands(tree, guild)
    setup_map_commands(tree, guild)