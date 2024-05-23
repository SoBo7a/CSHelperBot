from discord import Intents, Client, app_commands, Object
from bot.commands import setup_commands
from bot.utils.stats_database import init_db_stats
from bot.utils.play_database import init_db_play
from bot.utils.setup import setup_channels
from bot.utils.logging import get_cs_butler_logger


def setup_bot() -> Client:
    intents = Intents.default()
    intents.message_content = True
    intents.guilds = True
    intents.members = True

    client = Client(intents=intents)
    tree = app_commands.CommandTree(client)
    # ToDo: make it available to multiple guilds / assign id dynamically
    MY_GUILD = Object(id=885183686646042724)

    @client.event
    async def on_ready():
        logger = get_cs_butler_logger(log_level="INFO")
        logger.info(f'{client.user} is now running!')
        
        guild = client.get_guild(MY_GUILD.id)
        await setup_channels(guild)

        # tree.copy_global_to(guild=MY_GUILD) # Use this for development/testing of commands, since they get copied over immediatly this way
        await tree.sync(guild=MY_GUILD)

    init_db_stats()
    init_db_play()
    setup_commands(tree, MY_GUILD)


    return client
