import random
from typing import List
from discord import Guild, Member, VoiceChannel, utils, Embed
from bot.utils.translations import translate


async def get_voice_channels(guild: Guild):
    """
    Retrieve all voice channels in a guild.

    Args:
        guild (Guild): The guild to search for voice channels.

    Returns:
        List[VoiceChannel]: A list of voice channels in the guild.
    """
    voice_channels = [channel for channel in guild.channels if isinstance(channel, VoiceChannel)]
    return voice_channels


def create_teams(members: List[Member]):
    """
    Create two teams from a list of members.

    Args:
        members (List[Member]): The list of members to divide into teams.

    Returns:
        tuple[List[Member], List[Member]]: A tuple containing two lists of members representing the teams.
    """
    random.shuffle(members)
    mid_index = len(members) // 2
    team1 = members[:mid_index]
    team2 = members[mid_index:]
    return team1, team2


async def move_members(members: List[Member], target_channel: VoiceChannel):
    """
    Move members to a target voice channel.

    Args:
        members (List[Member]): The list of members to move.
        target_channel (VoiceChannel): The voice channel to move the members to.
    """
    for member in members:
        await member.move_to(target_channel)


async def create_and_move_teams(interaction) -> str:
    """
    Create teams and move members to respective channels.

    Args:
        interaction: The interaction object from Discord.

    Returns:
        str: A message indicating the outcome of the operation.
    """
    guild = interaction.guild
    cs2_channel = utils.get(guild.voice_channels, name='CS2')
    terrorist_channel = utils.get(guild.voice_channels, name='Terrorist')
    anti_terrorist_channel = utils.get(guild.voice_channels, name='Anti Terrorist')

    if cs2_channel and terrorist_channel and anti_terrorist_channel:
        members = cs2_channel.members
        team1, team2 = create_teams(members)

        # Create an embed
        embed = Embed(title=translate("commands.teams.embed_title"), color=0xFF5733)

        # Add fields for each team
        for team_name, team_members in [("Terrorists", team1), ("Anti Terrorists", team2)]:
            team_member_names = "\n".join([member.display_name for member in team_members])
            team_size = len(team_members)
            embed.add_field(name=f"**{team_name} ({team_size})**", value=team_member_names, inline=True)

        # Move members to respective channels
        await move_members(team1, terrorist_channel)
        await move_members(team2, anti_terrorist_channel)

        return embed
    else:
        return "Could not find the necessary voice channels ('CS2', 'Terrorist', 'Anti Terrorist')."


async def move_to_lobby(interaction) -> None:
    """
    Move all members from team channels back to the lobby.

    Args:
        interaction: The interaction object from Discord.
    """
    guild = interaction.guild
    cs2_channel = utils.get(guild.voice_channels, name='CS2')
    terrorist_channel = utils.get(guild.voice_channels, name='Terrorist')
    anti_terrorist_channel = utils.get(guild.voice_channels, name='Anti Terrorist')

    if cs2_channel and terrorist_channel and anti_terrorist_channel:
        for member in terrorist_channel.members + anti_terrorist_channel.members:
            await member.move_to(cs2_channel)
        await interaction.followup.send(translate("commands.teams.moved_back"))
    else:
        await interaction.followup.send("Could not find the necessary channels or you do not have permission to move members.")
