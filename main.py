import random
from typing import Final, List
from dotenv import dotenv_values
from discord import Intents, Client, Message, VoiceChannel, Guild, Member


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
        print("Creating and moving users to teams")

        # Find the CS2 voice channel
        guild = message.guild
        cs2_channel = None
        team1_channel = None
        team2_channel = None

        for vc in guild.voice_channels:
            if vc.name == 'CS2':
                cs2_channel = vc
            elif vc.name == 'Team 1':
                team1_channel = vc
            elif vc.name == 'Team 2':
                team2_channel = vc

        if cs2_channel and team1_channel and team2_channel:
            # Get all members in the CS2 channel
            members = cs2_channel.members

            if len(members) >= 2:
                # Create two teams
                team1, team2 = create_teams(members)

                # Move members to their respective team channels
                await move_members(team1, team1_channel)
                await move_members(team2, team2_channel)

                # Send a message with the teams
                team1_names = [member.display_name for member in team1]
                team2_names = [member.display_name for member in team2]

                response = (
                    "Teams created and members moved:\n"
                    f"Team 1: {', '.join(team1_names)} (moved to 'Team 1' voice channel)\n"
                    f"Team 2: {', '.join(team2_names)} (moved to 'Team 2' voice channel)"
                )
                await message.channel.send(response)
            else:
                await message.channel.send("Not enough members in the CS2 channel to create teams.")
        else:
            await message.channel.send("Could not find the necessary voice channels ('CS2', 'Team 1', 'Team 2').")


def main() -> None:
    client.run(token=TOKEN)
    

if __name__ == '__main__':
    main()