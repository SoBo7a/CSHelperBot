# ToDo: implement rate limiting
from discord import app_commands, Interaction, Forbidden, utils, VoiceChannel, Guild
from bot.utils.play_database import add_subscription, get_subscriptions, delete_subscriptions

async def get_voice_channels(guild: Guild):
    voice_channels = [channel for channel in guild.channels if isinstance(channel, VoiceChannel)]
    return voice_channels

def setup_play_commands(tree: app_commands.CommandTree, guild):    
    
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
        user = interaction.user

        if action not in ["subscribe", "unsubscribe", ""]:
            await interaction.response.send_message("Invalid action. Use 'subscribe' or 'unsubscribe'.", ephemeral=True)
            return

        if action == "subscribe":
            add_subscription(user_id, username)
            await interaction.response.send_message(f"{mention}, you have been subscribed to CS2 play notifications.", ephemeral=True)
            return

        if action == "unsubscribe":
            delete_subscriptions(user_id)
            await interaction.response.send_message(f"{mention}, you have been unsubscribed from CS2 play notifications.", ephemeral=True)
            return

        subscriptions = get_subscriptions()
        if (user_id, username) not in subscriptions:
            await interaction.response.send_message(f"{mention}, you are not subscribed to /play notifications. Use `/play subscribe` to subscribe.", ephemeral=True)
            return

        # Send message to all subscribed users
        subscribed_user_ids = [user_id for user_id, _ in subscriptions]
        failed_mentions = []
        for user_id, username in subscriptions:
            user = await interaction.client.fetch_user(int(user_id))
            if user:
                try:
                    cs2_channel = utils.get(interaction.guild.voice_channels, name='CS2')
                    if cs2_channel:
                        invite = await cs2_channel.create_invite(max_age=3600, max_uses=1)
                        # ToDo: dont send message and invite to command executor
                        await user.send(f"{mention} wants to play CS2! Join us in the CS2 voice channel: {invite.url}")
                    else:
                        await interaction.response.send_message("CS2 voice channel not found.", ephemeral=True)
                        return
                except Forbidden:
                    failed_mentions.append(user.mention)

        if failed_mentions:
            await interaction.response.send_message(
                f"{mention} wants to play CS2.\n"
                f"Can't invite the following users, due to their discord privacy settings: {', '.join(failed_mentions)}.",
                ephemeral=True
            )
        else:
            await interaction.response.send_message("Players have been invited.", ephemeral=True)
