from discord import app_commands, Interaction, Embed, utils
from bot.utils.stats import get_steam_user, get_steam_stats, get_value_by_key, get_best_map, get_best_weapon
from bot.utils.database.stats_database import add_user, get_steam_id
from bot.utils.translations import translate
import time
import urllib


# Dictionary to keep track of last used time
user_last_used = {}
cooldown_time = 1800 # 30 minutes = 1800 seconds

def setup_stats_commands(tree: app_commands.CommandTree, guild):
    """
    Set up the /stats command for managing and displaying CS2 stats.

    This function registers the /stats command, which allows users to set up their Steam ID and
    retrieve their CS2 game statistics, including total kills, total deaths, KD ratio, total time
    played, win rate, best map, and best weapon.

    Parameters:
    - tree (app_commands.CommandTree): The command tree to which the command will be added.
    - guild (discord.Guild): The guild for which the command is being set up.

    Command Description:
    - /stats: Manage CS2 stats.
      - setup_steamid: Provide your Steam ID to set it up for retrieving stats.
      - user: Provide a Steam ID to retrieve stats for a specific user without storing it.

    Example:
        setup_stats_commands(bot.tree, some_guild)
    """
    @tree.command(description=translate("commands.stats.description"))
    @app_commands.describe(setup_steamid=translate("commands.stats.choice_describe"), user=translate("commands.stats.choice_user_describe"))
    async def stats(interaction: Interaction, setup_steamid: str = None, user: str = None):
        discord_id = str(interaction.user.id)
        current_time = time.time()
        
        # Check if user is rate limited
        if setup_steamid is None and discord_id in user_last_used:
            user_info = user_last_used[discord_id]
            first_use_time = user_info['first_use_time']
            use_count = user_info['use_count']

            # Check if the user is within the cooldown period
            if current_time - first_use_time < cooldown_time and use_count >= 5:
                await interaction.response.send_message(translate("commands.stats.cooldown"), ephemeral=True)
                return
            # Reset the count and timestamp if more than cooldown_time have passed
            elif current_time - first_use_time >= cooldown_time:
                user_last_used[discord_id] = {'first_use_time': current_time, 'use_count': 0}

        # Initialize or update the command usage count and timestamp
        if discord_id not in user_last_used:
            user_last_used[discord_id] = {'first_use_time': current_time, 'use_count': 0}

        user_last_used[discord_id]['use_count'] += 1

        if setup_steamid:
            # If a Steam ID is provided, set it up
            discord_username = str(interaction.user)
            add_user(discord_id, discord_username, setup_steamid)
            await interaction.response.send_message(translate("commands.stats.steamId_setup").format(steamid=setup_steamid) + interaction.user.mention + ".", ephemeral=True)
        else:
            # Determine which Steam ID to use for stats retrieval
            steam_id_to_check = user if user else get_steam_id(discord_id)
            
            if steam_id_to_check:
                try:
                    stats_data = get_steam_stats(steam_id_to_check)
                except urllib.error.HTTPError as e:
                    if e.code == 403:
                        # Fetch the category by name
                        category = utils.get(interaction.guild.categories, name="CS2-Butler-Bot")
                        if category:
                            # Fetch the instructions channel within the category
                            instructions_channel = utils.get(category.text_channels, name=translate("instructions.instructions.channel.name"))
                            if instructions_channel:
                                channel_mention = instructions_channel.mention
                                await interaction.response.send_message(translate("commands.stats.privacy_settings_error").format(channel=channel_mention), ephemeral=True)
                            else:
                                await interaction.response.send_message("Instructions channel not found in the expected category. Please contact an admin.", ephemeral=True)
                        else:
                            await interaction.response.send_message("Category 'CS2-Butler-Bot' not found. Please contact an admin.", ephemeral=True)
                        return
                    else:
                        await interaction.response.send_message(f"Failed to retrieve stats data. Error: {e}", ephemeral=True)
                        return

                if stats_data is not None:
                    if 'playerstats' in stats_data and 'stats' in stats_data['playerstats']:
                        player_stats = stats_data['playerstats']['stats']
    
                        user_data = get_steam_user(steam_id_to_check)['response']['players'][0]
                        personaname = user_data['personaname']
                        profileurl = user_data['profileurl']
                        avatar_url = user_data['avatar']
                        
                        # Extracting specific values
                        total_kills = get_value_by_key(player_stats, 'total_kills')
                        total_deaths = get_value_by_key(player_stats, 'total_deaths')
                        kd_ratio = round(total_kills / total_deaths, 2)
                        total_time_played = str(round(get_value_by_key(player_stats, 'total_time_played') / 3600, 2)) + ' h'

                        # Extracting win/loss stats
                        total_matches_won = get_value_by_key(player_stats, 'total_matches_won')
                        total_matches_played = get_value_by_key(player_stats, 'total_matches_played')
                        if total_matches_played > 0:
                            win_rate = f'{(round(total_matches_won / total_matches_played, 2) * 100)} %'
                        else:
                            win_rate = '0 %'

                        # Finding the best map
                        best_map, highest_wins = get_best_map(player_stats)

                        # Finding the best weapon
                        best_weapon, highest_kills = get_best_weapon(player_stats)

                        # Create an embed                        
                        embed = Embed(title="CS2 Stats", description=f"for Player:\n**[{personaname}]({profileurl})**")
                        embed.set_thumbnail(url=avatar_url)
                        embed.add_field(name="Total Time Played", value=total_time_played, inline=True)
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
                        await interaction.response.send_message("Failed to retrieve object 'playerstats'")
                else:
                    await interaction.response.send_message("Failed to retrieve stats data.")
            else:
                await interaction.response.send_message(translate("commands.stats.steamId_missing"))
                