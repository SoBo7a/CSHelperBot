import urllib.request
import json
import config.settings as settings


def get_steam_stats(steam_id: str) -> dict:
    """
    Retrieves Steam statistics for a given Steam ID using the Steam API.

    Args:
        steam_id (str): The Steam ID of the user whose statistics are being retrieved.

    Returns:
        dict: A dictionary containing the Steam statistics data.
    """
    key = settings.STEAM_API_KEY
    appid = "730" # 730 for Counter Strike
    url = f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v2/?appid={appid}&key={key}&steamid={steam_id}"
    
    with urllib.request.urlopen(url) as response:
        data = response.read()
        return json.loads(data)
    

def get_value_by_key(stats_list, key):
    """
    Retrieves a specific value from a list of dictionaries based on the given key.

    Args:
        stats_list (list): A list of dictionaries containing statistics data.
        key (str): The key to search for in the dictionaries.

    Returns:
        Any: The value associated with the given key, or None if the key is not found.
    """
    for stats_dict in stats_list:
        if stats_dict.get('name') == key:
            return stats_dict.get('value')
    return None


def get_best_map(stats_list):
    """
    Finds the best map based on the total number of wins in the statistics data.

    Args:
        stats_list (list): A list of dictionaries containing statistics data.

    Returns:
        tuple: A tuple containing the name of the best map and the number of wins on that map.
    """
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


def get_best_weapon(stats_list):
    """
    Finds the best weapon based on the total number of kills with each weapon in the statistics data.

    Args:
        stats_list (list): A list of dictionaries containing statistics data.

    Returns:
        tuple: A tuple containing the name of the best weapon and the number of kills with that weapon.
    """
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