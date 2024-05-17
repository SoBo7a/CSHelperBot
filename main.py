import random
from typing import Final, List
from dotenv import dotenv_values
from discord import Intents, Client, Message, VoiceChannel, Guild, Member
import discord


# Load Token from .env
config = dotenv_values(".env")
TOKEN: Final[str] = config.get('TOKEN')

if not TOKEN:
    raise ValueError("No TOKEN found in environment variables. Make sure to set it in the .env file.")


# Setup Bot
intents: Intents = Intents.default()
intents.message_content = True  #NOQA
intents.guilds = True  # Ensure guild intents are enabled to access guild information
intents.members = True  # Enable intents to access member information
client: Client = Client(intents=intents)


# Get all voice channels in the guild
async def get_voice_channels(guild: Guild):
    voice_channels = [channel for channel in guild.channels if isinstance(channel, VoiceChannel)]
    return voice_channels


# Create two randomized teams from members
def create_teams(members: List[Member]):
    random.shuffle(members)
    mid_index = len(members) // 2
    team1 = members[:mid_index]
    team2 = members[mid_index:]
    return team1, team2

# Move members from one voice channel to another
async def move_members(members: List[Member], target_channel: VoiceChannel):
    for member in members:
        await member.move_to(target_channel)

        
# Bot startup
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')
    for guild in client.guilds:
        voice_channels = await get_voice_channels(guild)
        print(f'Voice channels in guild {guild.name}:')
        for channel in voice_channels:
            print(f' - {channel.name}')
    

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')

    # Check for the /teams command
    if user_message.lower() == '/teams' and channel == 'CS2':
        # Check if the author is an administrator
        if message.author.guild_permissions.administrator:
            print("Creating and moving users to teams")
            await create_and_move_teams(message)
        else:
            await message.channel.send("You do not have permission to use this command.")

    # Check for the /back command
    elif user_message.lower() == '/back':
        # Check if the author has permission to move members
        if message.author.guild_permissions.move_members:
            print("Moving users back to CS2")
            await move_to_lobby(message)
        else:
            await message.channel.send("You do not have permission to use this command.")


async def create_and_move_teams(message: Message) -> None:
    # Find the necessary voice channels
    guild = message.guild
    cs2_channel = discord.utils.get(guild.voice_channels, name='CS2')
    terrorist_channel = discord.utils.get(guild.voice_channels, name='Terrorist')
    anti_terrorist_channel = discord.utils.get(guild.voice_channels, name='Anti Terrorist')

    if cs2_channel and terrorist_channel and anti_terrorist_channel:
        # Get all members in the CS2 channel
        members = cs2_channel.members

        if len(members) >= 2:
            # Create two teams
            team1, team2 = create_teams(members)

            # Move members to their respective team channels
            await move_members(team1, terrorist_channel)
            await move_members(team2, anti_terrorist_channel)

            # Send a message with the teams
            team1_names = [member.display_name for member in team1]
            team2_names = [member.display_name for member in team2]

            response = (
                "Teams created and members moved:\n"
                f"Terrorist: {', '.join(team1_names)} (moved to 'Terrorist' voice channel)\n"
                f"Anti Terrorist: {', '.join(team2_names)} (moved to 'Anti Terrorist' voice channel)"
            )
            await message.channel.send(response)
        else:
            await message.channel.send("Not enough members in the CS2 channel to create teams.")
    else:
        await message.channel.send("Could not find the necessary voice channels ('CS2', 'Terrorist', 'Anti Terrorist').")


async def move_to_lobby(message: Message) -> None:
    # Find the necessary voice channels
    guild = message.guild
    cs2_channel = discord.utils.get(guild.voice_channels, name='CS2')
    terrorist_channel = discord.utils.get(guild.voice_channels, name='Terrorist')
    anti_terrorist_channel = discord.utils.get(guild.voice_channels, name='Anti Terrorist')

    # Check if the channels exist and the author has permission to move members
    if cs2_channel and terrorist_channel and anti_terrorist_channel and message.author.guild_permissions.move_members:
        # Move all members from Terrorist and Anti Terrorist channels to CS2
        for member in terrorist_channel.members + anti_terrorist_channel.members:
            await member.move_to(cs2_channel)
        await message.channel.send("Moved all members back to CS2.")
    else:
        await message.channel.send("Could not find the necessary channels or you do not have permission to move members.")



def main() -> None:
    client.run(token=TOKEN)
    

if __name__ == '__main__':
    main()