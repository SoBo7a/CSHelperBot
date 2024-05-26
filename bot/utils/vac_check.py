import urllib.response
import json
import asyncio
import config.settings as settings
from discord import Embed
from bot.utils.database.vac_check_database import get_vac_checks, delete_old_entries, remove_entry_by_steam_id
from bot.utils.stats import get_steam_user
from bot.utils.translations import translate


UPDATE_CYCLE = 24 # Interval (hours) in which we check for new vac bans


def get_vac_data(steamid: str):
    """
    Fetches VAC ban information from the Steam API for the specified Steam IDs.

    Args:
        steamid (str): The Steam IDs for which to retrieve VAC ban information.

    Returns:
        dict or None: A dictionary containing the VAC ban information for the specified Steam ID if successful,
                      or None if an error occurs during the request.
    """
    key = settings.STEAM_API_KEY
    url = f'https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key={key}&steamids={steamid}'

    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
            return json.loads(data)
    except urllib.error.HTTPError as e:
        if e.code == 403:
            raise e
        else:
            return None   
        

async def post_content(channel, steam_id, player_bans, discord_user_id):
    """
    Posts a message in the specified channel with information about the VAC ban.

    Args:
        channel (discord.TextChannel): The Discord channel where the message will be posted.
        steam_id (str): The Steam ID of the player who received the VAC ban.
        player_bans (dict): A dictionary containing information about the VAC ban.

    Returns:
        None
    """
    user_data = get_steam_user(steam_id)['response']['players'][0]
    personaname = user_data['personaname']
    profileurl = user_data['profileurl']
    avatar_url = user_data['avatar']  
    
    vac_banned = player_bans.get('VACBanned', False)
    number_of_vac_bans = player_bans.get('NumberOfVACBans', 0)
    number_of_game_bans = player_bans.get('NumberOfGameBans', 0)
    days_since_last_ban = player_bans.get('DaysSinceLastBan', 0)
    community_banned = player_bans.get('CommunityBanned', False)
    economy_ban = player_bans.get('EconomyBan', 'none')

    mention_msg = await channel.send(f"<@{discord_user_id}>")

    embed = Embed(title="New VAC Ban Detected", description=f"for Player:\n**[{personaname}]({profileurl})**")
    embed.set_thumbnail(url=avatar_url)
    embed.add_field(name="Steam ID", value=steam_id, inline=False)
    embed.add_field(name="Number of VAC Bans", value=number_of_vac_bans, inline=True)
    embed.add_field(name="Number of Game Bans", value=number_of_game_bans, inline=True)
    embed.add_field(name="Days Since Last Ban", value=days_since_last_ban, inline=True)
    embed.add_field(name="VAC Banned", value="Yes" if vac_banned else "No", inline=True)
    embed.add_field(name="Community Banned", value="Yes" if community_banned else "No", inline=True)
    embed.add_field(name="Economy Ban", value=economy_ban, inline=True)
    embed.add_field(name="", value=f"<@{discord_user_id}>")
        
    await channel.send(embed=embed)
    await mention_msg.delete()
    

async def check_for_bans(channel):
    """
    Checks for new VAC bans by fetching ban information from the Steam API for Steam IDs
    stored in the database. If new bans are detected, it posts a message in the specified channel with
    information about the ban and removes the corresponding entry from the database.

    Args:
        channel (discord.TextChannel): The Discord channel where ban notifications will be posted.

    Returns:
        None
    """
    delete_old_entries()
    
    # Fetch all entries from the database
    db_entries = get_vac_checks()
    if not db_entries:
        # print("No Steam IDs found in the database to check.") # For testing only!!!
        return
    
    # Extract all Steam IDs from the entries
    steam_ids = [entry[1] for entry in db_entries]
    
    # Join all Steam IDs into a comma-separated string
    steam_ids_str = ','.join(steam_ids)
    
    # Get the latest ban information for all Steam IDs using a single request
    vac_data = get_vac_data(steam_ids_str)
    
    if vac_data:
        # Iterate over each entry
        for entry in db_entries:
            discord_user_id, steam_id, check_date, number_of_vac_bans, days_since_last_ban = entry
            
            # Extract the ban information from the API response for the specific Steam ID
            player_bans = next((player for player in vac_data.get('players', []) if player.get('SteamId') == steam_id), None)
            
            if player_bans:
                latest_number_of_vac_bans = player_bans.get('NumberOfVACBans', 0)
                
                # Compare the ban information with the database
                if latest_number_of_vac_bans > number_of_vac_bans:
                    await post_content(channel, steam_id, player_bans, discord_user_id)
                    remove_entry_by_steam_id(steam_id)
                # For testing only!!!
                # else:
                #     await post_content(channel, steam_id, player_bans, discord_user_id) # For testing only!!!
                #     remove_entry_by_steam_id(steam_id) # For testing only!!!
                #     print(f"No new bans detected for Steam ID: {steam_id}") # For testing only!!!
            else:
                await channel.send(translate("commands.vac_check.description").format(steam_id=steam_id))
                remove_entry_by_steam_id(steam_id)
    else:
        await channel.send("[ERROR] Failed to retrieve ban information from the Steam API")


async def periodic_check_for_bans(channel):
    """
    Periodically checks for new VAC bans and prints any new bans found.
    This function runs indefinitely, checking for new bans once every X hours.

    Returns:
        None
    """
    while True:
        await check_for_bans(channel)
        await asyncio.sleep(UPDATE_CYCLE * 60 * 60)  # Update every X hours


async def start_periodic_check_for_bans(channel):
    """
    Starts the periodic check for new VAC bans when the bot starts up by creating an asynchronous task
    that runs the periodic_check_for_bans function.

    Returns:
        None
    """
    asyncio.create_task(periodic_check_for_bans(channel))