# ToDo: Implement error handling if user is not sharing game data
import urllib.request
import json
import config.settings as settings
from discord import app_commands, Interaction, Embed
from bot.utils.stats_database import add_user, get_steam_id

# Function to get the Steam stats
def get_steam_stats(steam_id: str) -> dict:
    key = settings.STEAM_API_KEY
    appid = "730"
    url = f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v2/?appid={appid}&key={key}&steamid={steam_id}"
    
    with urllib.request.urlopen(url) as response:
        data = response.read()
        return json.loads(data)
    
    
# Function to extract value by key from list of dictionaries
def get_value_by_key(stats_list, key):
    for stats_dict in stats_list:
        if stats_dict.get('name') == key:
            return stats_dict.get('value')
    return None


def setup_stats_commands(tree: app_commands.CommandTree, guild):

    @tree.command(description="Manage your CS2 Stats.")
    @app_commands.describe(steamid="Setup your Steam ID.")
    async def stats(interaction: Interaction, steamid: str = None):
        discord_id = str(interaction.user.id)

        if steamid:
            # If a Steam ID is provided, set it up
            discord_username = str(interaction.user)
            add_user(discord_id, discord_username, steamid)
            await interaction.response.send_message(f"Steam ID {steamid} has been set up for {interaction.user.mention}.")
        else:
            # If no Steam ID is provided, try to fetch and display the stored Steam ID
            stored_steam_id = get_steam_id(discord_id)
            if stored_steam_id:
                stats_data = get_steam_stats(stored_steam_id)
                if stats_data is not None:
                    if 'playerstats' in stats_data and 'stats' in stats_data['playerstats']:
                        player_stats = stats_data['playerstats']['stats']
                        
                        # Extracting specific values
                        total_kills = get_value_by_key(player_stats, 'total_kills')
                        total_deaths = get_value_by_key(player_stats, 'total_deaths')
                        kd_ratio = round(total_kills / total_deaths, 2)
                        total_time_played = round(get_value_by_key(player_stats, 'total_time_played') / 3600, 2)
                        
                        # Create an embed
                        embed = Embed(title="CS2 Stats", description=interaction.user.mention)
                        embed.add_field(name="Total Kills", value=total_kills, inline=True)
                        embed.add_field(name="Total Deaths", value=total_deaths, inline=True)
                        embed.add_field(name="KD Ratio", value=kd_ratio, inline=True)
                        embed.add_field(name="Total Time Played (Hours)", value=total_time_played, inline=True)
                        
                        # Send the embed
                        await interaction.response.send_message(embed=embed)
                    else:
                        await interaction.response.send_message(f"Failed to retrieve stats for Steam ID: **{stored_steam_id}**")
                else:
                    await interaction.response.send_message("Failed to retrieve stats data.")
            else:
                await interaction.response.send_message("You have not set up your Steam ID yet. Use `/stats steamid YOUR_STEAM_ID` to set it up.")
