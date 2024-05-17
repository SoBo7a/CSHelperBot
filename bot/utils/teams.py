import random
from typing import List
from discord import Guild, Member, VoiceChannel, utils, Embed


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
        team1, team2 = create_teams(members)

        # Create an embed
        embed = Embed(title="Teams created and members moved", color=0xFF5733)

        # Add fields for each team
        for team_name, team_members in [("Terrorists", team1), ("Anti Terrorists", team2)]:
            team_member_names = "\n".join([member.display_name for member in team_members])
            embed.add_field(name=f"**{team_name}**", value=team_member_names, inline=True)

        # Move members to respective channels
        await move_members(team1, terrorist_channel)
        await move_members(team2, anti_terrorist_channel)

        return embed
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
        await interaction.followup.send("Moved all members back to CS2.")
    else:
        await interaction.followup.send("Could not find the necessary channels or you do not have permission to move members.")
