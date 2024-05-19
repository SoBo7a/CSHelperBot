from discord import app_commands, Interaction, Forbidden, utils, VoiceChannel, Guild
from bot.utils.play_database import add_subscription, get_subscriptions, delete_subscriptions
from time import time


# Dictionary to store user IDs and their last request timestamps
cooldowns = {}


async def get_voice_channels(guild: Guild):
    """
    Retrieves all voice channels in the given guild.

    Parameters:
    - guild (discord.Guild): The guild from which to retrieve voice channels.

    Returns:
    - list: A list of VoiceChannel objects in the guild.
    """
    voice_channels = [channel for channel in guild.channels if isinstance(channel, VoiceChannel)]
    return voice_channels


def setup_play_commands(tree: app_commands.CommandTree, guild):    
    """
    Set up the /play command for managing CS2 play notifications and sending play invites.

    This function registers the /play command, which allows users to subscribe to or unsubscribe from 
    notifications for CS2 play sessions, and to notify subscribed users when someone wants to play.

    Parameters:
    - tree (app_commands.CommandTree): The command tree to which the command will be added.
    - guild (discord.Guild): The guild for which the command is being set up.

    Command Description:
    - /play: Manage CS2 play notifications or notify others to play.
      - action (optional): Choose 'subscribe' to subscribe or 'unsubscribe' to unsubscribe from play notifications.
        - Subscribe: Subscribes the user to CS2 play notifications.
        - Unsubscribe: Unsubscribes the user from CS2 play notifications.
      - If no action is specified, it will send play invites to all subscribed users.

    Cooldown:
    - Prevents the user from spamming the /play command by enforcing a cooldown period of 180 seconds.

    Permissions:
    - Only users who are subscribed will receive play notifications.

    Example:
        setup_play_commands(bot.tree, some_guild)
    """
    @tree.command(description="Let everyone know you want to play CS2 or manage your subscription.")
    @app_commands.describe(action="Choose 'subscribe' to subscribe or 'unsubscribe' to unsubscribe from play notifications for CS2")
    @app_commands.choices(action=[
        app_commands.Choice(name="Subscribe", value="subscribe"),
        app_commands.Choice(name="Unsubscribe", value="unsubscribe")
    ])
    async def play(interaction: Interaction, action: str = ""):
        mention = interaction.user.mention
        user_id = str(interaction.user.id)
        username = str(interaction.user)

        # Check if the action is subscribe or unsubscribe
        if action in ["subscribe", "unsubscribe"]:
            if action == "subscribe":
                add_subscription(user_id, username)
                await interaction.response.send_message(f"{mention}, you have been subscribed to CS2 play notifications.", ephemeral=True)
            elif action == "unsubscribe":
                delete_subscriptions(user_id)
                await interaction.response.send_message(f"{mention}, you have been unsubscribed from CS2 play notifications.", ephemeral=True)
            return

        # Check if user is on cooldown
        if user_id in cooldowns:
            last_request_time = cooldowns[user_id]
            elapsed_time = time() - last_request_time
            if elapsed_time < 180:  # Cooldown period in seconds
                await interaction.response.send_message(f"{mention}, you are on cooldown. Please wait before using this command again.", ephemeral=True)
                return

        # Update cooldown
        cooldowns[user_id] = time()

        # Check if the user is subscribed
        subscriptions = get_subscriptions()
        if (user_id, username) not in subscriptions:
            await interaction.response.send_message(f"{mention}, you are not subscribed to /play notifications. Use `/play subscribe` to subscribe.", ephemeral=True)
            return

        await interaction.response.send_message("Sending invites...", ephemeral=True)

        # Send message to all subscribed users
        failed_mentions = []
        for sub_user_id, _ in subscriptions:
            if user_id != sub_user_id:
                try:
                    sub_user = await interaction.client.fetch_user(int(sub_user_id))
                    cs2_channel = utils.get(interaction.guild.voice_channels, name='CS2')
                    if cs2_channel:
                        invite = await cs2_channel.create_invite(max_age=3600, max_uses=1)
                        await sub_user.send(f"{mention} wants to play CS2! Join us in the CS2 voice channel: {invite.url}")
                    else:
                        await interaction.followup.send("CS2 voice channel not found.", ephemeral=True)
                        return
                except Forbidden:
                    failed_mentions.append(sub_user.mention)

        if failed_mentions:
            await interaction.followup.send(
                f"{mention} wants to play CS2.\n"
                f"Can't invite the following users, due to their discord privacy settings: {', '.join(failed_mentions)}.",
            )
        else:
            await interaction.followup.send("Players have been invited.")
