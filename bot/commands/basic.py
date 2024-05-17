from discord import app_commands, Interaction, Member, utils
from typing import Optional

def setup_basic_commands(tree: app_commands.CommandTree, guild):
    @tree.command()
    async def hello(interaction: Interaction):
        """Says hello!"""
        await interaction.response.send_message(f'Hi, {interaction.user.mention}')

    @tree.command()
    @app_commands.describe(
        first_value='The first value you want to add something to',
        second_value='The value you want to add to the first value',
    )
    async def add(interaction: Interaction, first_value: int, second_value: int):
        """Adds two numbers together."""
        await interaction.response.send_message(f'{first_value} + {second_value} = {first_value + second_value}')
    
    @tree.command()
    @app_commands.describe(member='The member you want to get the joined date from; defaults to the user who uses the command')
    async def joined(interaction: Interaction, member: Optional[Member] = None):
        """Says when a member joined."""
        member = member or interaction.user
        await interaction.response.send_message(f'{member} joined {utils.format_dt(member.joined_at)}')
