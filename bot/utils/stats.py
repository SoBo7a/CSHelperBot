import urllib.request
import json
import config.settings as settings


def get_steam_user(steam_id: str) -> dict:
    key = settings.STEAM_API_KEY
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?format=json&key={key}&steamids={steam_id}"
        
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
            return json.loads(data)
    except urllib.error.HTTPError as e:
        if e.code == 403:
            raise e
        else:
            return None
    

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
    
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
            return json.loads(data)
    except urllib.error.HTTPError as e:
        if e.code == 403:
            raise e
        else:
            return None
    

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
    Finds the best map based on the win rate in the statistics data,
    considering only maps with rounds played at or below 70% of the average rounds played.

    Args:
        stats_list (list): A list of dictionaries containing statistics data.

    Returns:
        tuple: A tuple containing the name of the best map and the win rate on that map.
    """
    map_rounds = {}
    total_rounds = 0
    map_count = 0
    
    # Calculate total rounds and map count for average rounds calculation
    for stats_dict in stats_list:
        rounds_key = stats_dict.get('name')
        if rounds_key and rounds_key.startswith('total_rounds_map_'):
            map_name = rounds_key.split('_')[-2] + "_" + rounds_key.split('_')[-1]
            rounds = stats_dict.get('value')
            map_rounds[map_name] = rounds
            total_rounds += rounds
            map_count += 1

    # Calculate average rounds played
    if map_count == 0:
        return None, 0
    average_rounds = total_rounds / map_count
    threshold_rounds = average_rounds * 0.7
    
    best_map = None
    highest_win_rate = -1
    
    for stats_dict in stats_list:
        wins_key = stats_dict.get('name')
        if wins_key and wins_key.startswith('total_wins_map_'):
            map_name = wins_key.split('_')[-2] + "_" + wins_key.split('_')[-1]
            rounds = map_rounds.get(map_name, 0)
            if rounds >= threshold_rounds:
                rounds_key = f"total_rounds_map_{map_name}"
                wins = stats_dict.get('value')
                rounds = next((sd.get('value') for sd in stats_list if sd.get('name') == rounds_key), 0)
                if rounds > 0:
                    win_rate = wins / rounds
                    if win_rate > highest_win_rate:
                        highest_win_rate = win_rate
                        best_map = map_name

    return best_map, highest_win_rate


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