from discord import app_commands, Interaction, Embed
from bot.utils.stats import get_steam_stats, get_value_by_key, get_best_map, get_best_weapon
from bot.utils.stats_database import add_user, get_steam_id


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
      - steamid: Provide your Steam ID to set it up for retrieving stats.
        - If provided, the command will save the Steam ID for the user.

    Example:
        setup_stats_commands(bot.tree, some_guild)
    """
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
                        await interaction.response.send_message("Failed to retrieve object 'playerstats'")
                else:
                    await interaction.response.send_message("Failed to retrieve stats data.")
            else:
                await interaction.response.send_message("You have not set up your Steam ID yet. Use `/stats steamid YOUR_STEAM_ID` to set it up.")
