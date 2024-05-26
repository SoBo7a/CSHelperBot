from discord import app_commands, Interaction, Embed
from bot.utils.database.vac_check_database import insert_vac_check, steam_id_exists
from bot.utils.stats import get_steam_user
from bot.utils.vac_check import get_vac_data
from bot.utils.translations import translate


# Command to check VAC bans
def setup_vac_check_commands(tree: app_commands.CommandTree, guild):
    """
    Sets up a Discord bot command to check the VAC ban status for a given Steam ID.

    This function defines a Discord bot command named 'vac_check' that allows users to check the VAC ban status
    for a specified Steam ID. It creates a database entry for the provided Steam ID, which lasts for 360 days,
    and sets up daily checks for new VAC bans. If any Steam ID receives a VAC ban during this period, a message
    will be sent in the corresponding channel.

    Args:
        tree (app_commands.CommandTree): The CommandTree instance representing the command tree of the Discord bot.
        guild (discord.Guild): The Discord guild (server) where the command will be added.

    Returns:
        None
    """
    @app_commands.command(name="vac_check", description=translate("commands.vac_check.description"))
    @app_commands.describe(steamid=translate("commands.vac_check.describe"))
    async def vac_check(interaction: Interaction, steamid: str): 
           
        if steam_id_exists(steamid):
            await interaction.response.send_message(translate("commands.vac_check.steamid_exists"), ephemeral=True)
            return  
        
        try:
            user_data = get_steam_user(steamid)['response']['players'][0]
        except IndexError:
            await interaction.response.send_message(translate("commands.vac_check.invalid_input").format(url=f"[SteamREP](https://steamrep.com/search?q={steamid})"), ephemeral=True)
            return
        
        personaname = user_data['personaname']
        profileurl = user_data['profileurl']
        avatar_url = user_data['avatar']  
        
        data = get_vac_data(steamid)
        player_bans = data.get('players', [])[0]

        if player_bans:
            vac_banned = player_bans.get('VACBanned', False)
            number_of_vac_bans = player_bans.get('NumberOfVACBans', 0)
            number_of_game_bans = player_bans.get('NumberOfGameBans', 0)
            days_since_last_ban = player_bans.get('DaysSinceLastBan', 0)
            community_banned = player_bans.get('CommunityBanned', False)
            economy_ban = player_bans.get('EconomyBan', 'none')

            embed = Embed(title="VAC Ban Check", description=f"for Player:\n**[{personaname}]({profileurl})**")
            embed.set_thumbnail(url=avatar_url)
            embed.add_field(name="Steam ID", value=steamid, inline=False)
            embed.add_field(name="Number of VAC Bans", value=number_of_vac_bans, inline=True)
            embed.add_field(name="Number of Game Bans", value=number_of_game_bans, inline=True)
            embed.add_field(name="Days Since Last Ban", value=days_since_last_ban, inline=True)
            embed.add_field(name="VAC Banned", value="Yes" if vac_banned else "No", inline=True)
            embed.add_field(name="Community Banned", value="Yes" if community_banned else "No", inline=True)
            embed.add_field(name="Economy Ban", value=economy_ban, inline=True)
            embed.add_field(name="VAC-Watch Status", value=translate("commands.vac_check.watch_status"), inline=False)
            
            insert_vac_check(interaction.user.id, steamid, number_of_vac_bans, days_since_last_ban)

            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(translate("commands.vac_check.no_information"), ephemeral=True)
               
    tree.add_command(vac_check, guild=guild)