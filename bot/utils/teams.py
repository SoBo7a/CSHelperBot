import random
from typing import List
from discord import Guild, Member, VoiceChannel, utils

async def get_voice_channels(guild: Guild):
    voice_channels = [channel for channel in guild.channels if isinstance(channel, VoiceChannel)]
    return voice_channels

def create_teams(members: List[Member]):
    random.shuffle(members)
    mid_index = len(members) // 2
    team1 = members[:mid_index]
    team2 = members[mid_index:]
    return team1, team2

async def move_members(members: List[Member], target_channel: VoiceChannel):
    for member in members:
        await member.move_to(target_channel)

async def create_and_move_teams(interaction) -> str:
    guild = interaction.guild
    cs2_channel = utils.get(guild.voice_channels, name='CS2')
    terrorist_channel = utils.get(guild.voice_channels, name='Terrorist')
    anti_terrorist_channel = utils.get(guild.voice_channels, name='Anti Terrorist')

    if cs2_channel and terrorist_channel and anti_terrorist_channel:
        members = cs2_channel.members
        if len(members) >= 2:
            team1, team2 = create_teams(members)
            await move_members(team1, terrorist_channel)
            await move_members(team2, anti_terrorist_channel)

            team1_names = [member.display_name for member in team1]
            team2_names = [member.display_name for member in team2]

            response = (
                "Teams created and members moved:\n"
                f"Terrorist: {', '.join(team1_names)} (moved to 'Terrorist' voice channel)\n"
                f"Anti Terrorist: {', '.join(team2_names)} (moved to 'Anti Terrorist' voice channel)"
            )
            return response
        else:
            return "Not enough members in the CS2 channel to create teams."
    else:
        return "Could not find the necessary voice channels ('CS2', 'Terrorist', 'Anti Terrorist')."

async def move_to_lobby(interaction) -> None:
    guild = interaction.guild
    cs2_channel = utils.get(guild.voice_channels, name='CS2')
    terrorist_channel = utils.get(guild.voice_channels, name='Terrorist')
    anti_terrorist_channel = utils.get(guild.voice_channels, name='Anti Terrorist')

    if cs2_channel and terrorist_channel and anti_terrorist_channel:
        for member in terrorist_channel.members + anti_terrorist_channel.members:
            await member.move_to(cs2_channel)
        await interaction.response.send_message("Moved all members back to CS2.")
    else:
        await interaction.response.send_message("Could not find the necessary channels or you do not have permission to move members.")
