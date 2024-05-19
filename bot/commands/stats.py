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

# Function to find the best map
def get_best_map(stats_list):
    best_map = None
    highest_wins = -1
    
    for stats_dict in stats_list:
        name = stats_dict.get('name')
        if name and name.startswith('total_wins_map_'):
            wins = stats_dict.get('value')
            if wins > highest_wins:
                highest_wins = wins
                best_map = name.split('_')[-2] + "_" + name.split('_')[-1]
    
    return best_map, highest_wins

# Function to find the best weapon
def get_best_weapon(stats_list):
    best_weapon = None
    highest_kills = -1
    
    for stats_dict in stats_list:
        name = stats_dict.get('name')
        if name and name.startswith('total_kills_') and name not in ["total_kills_headshot", "total_kills_enemy_weapon"]:
            kills = stats_dict.get('value')
            if kills > highest_kills:
                highest_kills = kills
                best_weapon = name.split('_')[-1]
    
    return best_weapon, highest_kills

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

                        # Extracting win/loss stats
                        total_matches_won = get_value_by_key(player_stats, 'total_matches_won')
                        total_matches_played = get_value_by_key(player_stats, 'total_matches_played')
                        if total_matches_played > 0:
                            win_rate = f'{(round(total_matches_won / total_matches_played, 2))} %'
                        else:
                            win_rate = '0 %'

                        # Finding the best map
                        best_map, highest_wins = get_best_map(player_stats)

                        # Finding the best weapon
                        best_weapon, highest_kills = get_best_weapon(player_stats)

                        # Create an embed
                        embed = Embed(title="CS2 Stats", description=interaction.user.mention)
                        embed.add_field(name="Total Time Played (Hours)", value=total_time_played, inline=True)
                        embed.add_field(name="Best Map", value=best_map, inline=True)
                        embed.add_field(name="Best Weapon", value=best_weapon, inline=True)
                        embed.add_field(name="Total Kills", value=total_kills, inline=True)
                        embed.add_field(name="Total Deaths", value=total_deaths, inline=True)
                        embed.add_field(name="KD Ratio", value=kd_ratio, inline=True)
                        embed.add_field(name="Total Matches Won", value=total_matches_won, inline=True)
                        embed.add_field(name="Total Matches Played", value=total_matches_played, inline=True)
                        embed.add_field(name="Win Rate", value=win_rate, inline=True)
                        
                        # Send the embed
                        await interaction.response.send_message(embed=embed)
                    else:
                        await interaction.response.send_message(f"Failed to retrieve stats for Steam ID: **{stored_steam_id}**")
                else:
                    await interaction.response.send_message("Failed to retrieve stats data.")
            else:
                await interaction.response.send_message("You have not set up your Steam ID yet. Use `/stats steamid YOUR_STEAM_ID` to set it up.")
