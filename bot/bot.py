import discord
from discord import Intents, Client, app_commands
from bot.commands import setup_commands
from bot.utils.stats_database import init_db_stats
from bot.utils.play_database import init_db_play


def setup_bot() -> Client:
    intents = Intents.default()
    intents.message_content = True
    intents.guilds = True
    intents.members = True

    client = Client(intents=intents)
    tree = app_commands.CommandTree(client)
    MY_GUILD = discord.Object(id=885183686646042724)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        tree.copy_global_to(guild=MY_GUILD) # ToDo: just for development, change for production!!!
        await tree.sync(guild=MY_GUILD)

    init_db_stats()
    init_db_play()
    setup_commands(tree, MY_GUILD)

    return client
