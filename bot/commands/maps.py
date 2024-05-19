from discord import app_commands, Interaction
from bot.utils.maps import get_random_map, cs2_maps, wingman_maps

def setup_map_commands(tree: app_commands.CommandTree, guild):
    """
    Set up the /map command for selecting a random CS2 map.

    This function registers the /map command, which allows users to choose a 
    random CS2 map from either the standard or wingman map pools.

    Parameters:
    - tree (app_commands.CommandTree): The command tree to which the command will be added.
    - guild (discord.Guild): The guild for which the command is being set up.

    Command Description:
    - /map: Selects a random CS2 map.
      - mode (optional): Choose between standard or wingman maps.
        - Standard: Selects a random map from the standard map pool.
        - Wingman: Selects a random map from the wingman map pool.

    Example:
        setup_map_commands(bot.tree, some_guild)
    """
    @tree.command(description="Selects a random CS2 map.")
    @app_commands.describe(mode="Choose between standard or wingman maps.")
    @app_commands.choices(mode=[
        app_commands.Choice(name="Standard", value="standard"),
        app_commands.Choice(name="Wingman", value="wingman")
    ])
    async def map(interaction: Interaction, mode: str = "standard"):
        if mode == "wingman":
            random_map = get_random_map(wingman_maps)
        else:
            random_map = get_random_map(cs2_maps)

        await interaction.response.send_message(f"The selected map is: **{random_map}**")