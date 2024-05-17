import random
from typing import Final, List, Optional
from dotenv import dotenv_values
from discord import Intents, Client, Message, VoiceChannel, Guild, Member, app_commands
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

### Slash Examples ###

tree = app_commands.CommandTree(client)

MY_GUILD = discord.Object(id=885183686646042724)


@tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')


@tree.command()
@app_commands.describe(
    first_value='The first value you want to add something to',
    second_value='The value you want to add to the first value',
)
async def add(interaction: discord.Interaction, first_value: int, second_value: int):
    """Adds two numbers together."""
    await interaction.response.send_message(f'{first_value} + {second_value} = {first_value + second_value}')
    
    
# To make an argument optional, you can either give it a supported default argument
# or you can mark it as Optional from the typing standard library. This example does both.
@tree.command()
@app_commands.describe(member='The member you want to get the joined date from; defaults to the user who uses the command')
async def joined(interaction: discord.Interaction, member: Optional[discord.Member] = None):
    """Says when a member joined."""
    # If no member is explicitly provided then we use the command user here
    member = member or interaction.user

    # The format_dt function formats the date time into a human readable representation in the official client
    await interaction.response.send_message(f'{member} joined {discord.utils.format_dt(member.joined_at)}')

### Slash Examples End ###


@tree.command()
async def teams(interaction: discord.Interaction):
    """Creates and moves users to teams."""
    # Check if the author is an administrator
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You do not have permission to use this command.")
        return

    # Check if the user is in the 'CS2' voice channel
    if str(interaction.channel) != 'CS2':
        await interaction.response.send_message("You need to be in the 'CS2' voice channel to use this command.")
        return

    statusMsg = await create_and_move_teams(interaction)
    await interaction.response.send_message(statusMsg)
    return


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
    
    tree.copy_global_to(guild=MY_GUILD)
    await tree.sync(guild=MY_GUILD)
        
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

    # ToDo: Convert to slash command
    # Check for the /back command
    if user_message.lower() == '/back':
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
            # await message.channel.send(response)
            return response
        else:
            # await message.channel.send("Not enough members in the CS2 channel to create teams.")
            return "Not enough members in the CS2 channel to create teams."
    else:
        # await message.channel.send("Could not find the necessary voice channels ('CS2', 'Terrorist', 'Anti Terrorist').")
        return "Could not find the necessary voice channels ('CS2', 'Terrorist', 'Anti Terrorist')."


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