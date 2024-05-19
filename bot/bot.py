from discord import Intents, Client, app_commands, Object
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
    MY_GUILD = Object(id=885183686646042724)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        
        # In this basic example, we just synchronize the app commands to one guild.
        # Instead of specifying a guild to every command, we copy over our global commands instead.
        # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
        tree.copy_global_to(guild=MY_GUILD)
        await tree.sync(guild=MY_GUILD)

    init_db_stats()
    init_db_play()
    setup_commands(tree, MY_GUILD)

    return client
