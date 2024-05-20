from discord import Guild, utils, File
from .translations import translate
import os


base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
empty_line = "\u200B"


async def send_tutorial(instructions_channel):
    # Send the headline
    await instructions_channel.send(translate('instructions.headline'))

    # Feature: /teams
    teams_message = await instructions_channel.send(translate('instructions.teams.description'))
    teams_thread = await teams_message.create_thread(name="Feature 1: /teams")
    teams_image_path = os.path.join(base_dir, 'assets', 'img', 'Tutorial_teams.png')
    with open(teams_image_path, 'rb') as f:
        picture = File(f, spoiler=True)
        await teams_thread.send(file=picture)

    # Feature: /play
    play_message = await instructions_channel.send(translate('instructions.play.description'))
    play_thread = await play_message.create_thread(name="Feature 2: /play")
    await play_thread.send(translate('instructions.play.sub_notifications'))
    play_image1 = os.path.join(base_dir, 'assets', 'img', 'Tutorial_play_sub1.png')
    with open(play_image1, 'rb') as f:
        picture = File(f, spoiler=True)
        await play_thread.send(file=picture)
    play_image2 = os.path.join(base_dir, 'assets', 'img', 'Tutorial_play_sub2.png')
    with open(play_image2, 'rb') as f:
        picture = File(f, spoiler=True)
        await play_thread.send(file=picture)
    await play_thread.send(translate('instructions.play_sub1'))
    play_image3 = os.path.join(base_dir, 'assets', 'img', 'Tutorial_play_sub3.png')
    with open(play_image3, 'rb') as f:
        picture = File(f, spoiler=True)
        await play_thread.send(file=picture)
    await play_thread.send(translate('instructions.play_sub2'))
    play_image4 = os.path.join(base_dir, 'assets', 'img', 'Tutorial_play_sub4.png')
    with open(play_image4, 'rb') as f:
        picture = File(f, spoiler=True)
        await play_thread.send(file=picture)
    await play_thread.send(translate('instructions.play_usage'))
    play_image5 = os.path.join(base_dir, 'assets', 'img', 'Tutorial_play_sub5.png')
    with open(play_image5, 'rb') as f:
        picture = File(f, spoiler=True)
        await play_thread.send(file=picture)

    # Feature: /map
    map_message = await instructions_channel.send(translate('instructions.map.description'))
    map_thread = await map_message.create_thread(name="Feature 3: /map")
    await map_thread.send(translate('instructions.map.instructions'))
    map_image1 = os.path.join(base_dir, 'assets', 'img', 'Tutorial_map1.png')
    with open(map_image1, 'rb') as f:
        picture = File(f, spoiler=True)
        await map_thread.send(file=picture)
    map_image2 = os.path.join(base_dir, 'assets', 'img', 'Tutorial_map2.png')
    with open(map_image2, 'rb') as f:
        picture = File(f, spoiler=True)
        await map_thread.send(file=picture)
    map_image3 = os.path.join(base_dir, 'assets', 'img', 'Tutorial_map3.png')
    with open(map_image3, 'rb') as f:
        picture = File(f, spoiler=True)
        await map_thread.send(file=picture)

    # Feature: /stats
    stats_message = await instructions_channel.send(translate("instructions.stats.description"))
    stats_thread = await stats_message.create_thread(name="Feature 4: /stats")
    await stats_thread.send(translate("instructions.stats.usage"))
    stats_image0 = os.path.join(base_dir, 'assets', 'img', 'Tutorial_stats_steamid.png')
    with open(stats_image0, 'rb') as f:
        picture = File(f, spoiler=True)
        await stats_thread.send(file=picture)
    await stats_thread.send(translate("instructions.stats.privacy_settings"))
    stats_image1 = os.path.join(base_dir, 'assets', 'img', 'Tutorial_stats_steamid1.png')
    with open(stats_image1, 'rb') as f:
        picture = File(f, spoiler=True)
        await stats_thread.send(file=picture)
    await stats_thread.send(translate("instructions.stats.link_steamID"))
    stats_image2 = os.path.join(base_dir, 'assets', 'img', 'Tutorial_stats_steamid2.png')
    with open(stats_image2, 'rb') as f:
        picture = File(f, spoiler=True)
        await stats_thread.send(file=picture)
    stats_image3 = os.path.join(base_dir, 'assets', 'img', 'Tutorial_stats_steamid3.png')
    with open(stats_image3, 'rb') as f:
        picture = File(f, spoiler=True)
        await stats_thread.send(file=picture)
    await stats_thread.send(translate("instructions.stats.link_steamID"))
    stats_image4 = os.path.join(base_dir, 'assets', 'img', 'Tutorial_stats_steamid4.png')
    with open(stats_image4, 'rb') as f:
        picture = File(f, spoiler=True)
        await stats_thread.send(file=picture)
    stats_image5 = os.path.join(base_dir, 'assets', 'img', 'Tutorial_stats_steamid5.png')
    with open(stats_image5, 'rb') as f:
        picture = File(f, spoiler=True)
        await stats_thread.send(file=picture)
    await stats_thread.send(translate("instructions.stats.usage_complete"))
    stats_image6 = os.path.join(base_dir, 'assets', 'img', 'Tutorial_stats_steamid6.png')
    with open(stats_image6, 'rb') as f:
        picture = File(f, spoiler=True)
        await stats_thread.send(file=picture)
        
    await instructions_channel.send(empty_line)

    # Conclusion    
    mention = f"<@693204479259967559>"
    github_link = "https://github.com/SoBo7a/CSHelperBot"
    contact_support_message = translate("instructions.contact_support").format(mention=mention, github_link=github_link)
    await instructions_channel.send(contact_support_message)
    await instructions_channel.send("@everyone")
    

async def setup_channels(guild: Guild):    
    # Check for bot category and create it if it doesn't exist
    category = utils.get(guild.categories, name='CS2-Butler-Bot')
    if not category:
        category = await guild.create_category('CS2-Butler-Bot')
        
        # Set the category's position to be just below the top position
        top_position = guild.categories[0].position
        await category.edit(position=top_position)
        
        # Create the Instructions channel if it doesn't exist
        instructions_channel = utils.get(guild.text_channels, name=translate("instructions.instructions.channel.name"))
        if not instructions_channel:
            instructions_channel = await guild.create_text_channel(translate("instructions.instructions.channel.name"), category=category)
            await instructions_channel.edit(topic=translate('instructions.topic_instructions'))

            # Set channel permissions for Instructions channel
            everyone_role = utils.get(guild.roles, name="@everyone")
            await instructions_channel.set_permissions(everyone_role, read_messages=True, send_messages=False)
            
            admin_role = utils.get(guild.roles, name="Admin")
            if admin_role:
                await instructions_channel.set_permissions(admin_role, send_messages=True)

            # Send a message to the Instructions channel
            await send_tutorial(instructions_channel)
            
        # Create the Commands channel if it doesn't exist
        commands_channel = utils.get(guild.text_channels, name='Commands')
        if not commands_channel:
            commands_channel = await guild.create_text_channel('Commands', category=category)
            await commands_channel.edit(topic=translate('instructions.topic_commands'))

            # Set channel permissions for Commands channel
            await commands_channel.set_permissions(everyone_role, read_messages=True, send_messages=True)
