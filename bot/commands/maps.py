from discord import app_commands, Interaction
from bot.utils.maps import get_random_map, cs2_maps, wingman_maps

def setup_map_commands(tree: app_commands.CommandTree, guild):

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