from discord import Guild, utils
from .translations import translate
from .tutorial import send_tutorial
from .patchnotes import post_initial_patchnotes, start_patchnote_check
        
        
async def setup_channels(guild: Guild):    
    """
    Sets up the category and its channels for the CS2 Butler Bot within the specified guild.

    Args:
        guild (discord.Guild): The Discord guild where channels will be set up.

    Returns:
        None
    """
    everyone_role = utils.get(guild.roles, name="@everyone")
    admin_role = utils.get(guild.roles, name="Admin")

    category = utils.get(guild.categories, name='CS2-Butler-Bot')
    channels_in_category = [channel for channel in guild.text_channels if channel.category_id == category.id] if category else []
        
    # Check for bot category and create it if it doesn't exist
    if not category:
        category = await guild.create_category('CS2-Butler-Bot')
        
        # Set the category's position to be just below the top position
        top_position = guild.categories[0].position
        await category.edit(position=top_position)
        
        
    # Create the Instructions channel if it doesn't exist
    if not any(translate("instructions.instructions.channel.name") == channel.name for channel in channels_in_category):
        instructions_channel = await guild.create_text_channel(translate("instructions.instructions.channel.name"), category=category)
        await instructions_channel.edit(topic=translate('instructions.topic_instructions'))

        # Set channel permissions for Instructions channel
        await instructions_channel.set_permissions(everyone_role, read_messages=True, send_messages=False)
        
        if admin_role:
            await instructions_channel.set_permissions(admin_role, send_messages=True)

        # Send a message to the Instructions channel
        await send_tutorial(instructions_channel)
            
        
    # Create the Commands channel if it doesn't exist
    if not any('commands' == channel.name for channel in channels_in_category):
        commands_channel = await guild.create_text_channel('commands', category=category)
        await commands_channel.edit(topic=translate('instructions.topic_commands'))

        # Set channel permissions for Commands channel
        await commands_channel.set_permissions(everyone_role, read_messages=True, send_messages=True)
            
            
    # Create the CS2 Patchnotes channel if it doesn't exist
    if not any('cs2-patchnotes' == channel.name for channel in channels_in_category):
        patchnotes_channel = await guild.create_text_channel('cs2-patchnotes', category=category)
        await patchnotes_channel.edit(topic="Latest CS2 Patchnotes and Updates")

        # Set channel permissions for Patchnotes channel
        await patchnotes_channel.set_permissions(everyone_role, read_messages=True, send_messages=False)
        
        if admin_role:
            await patchnotes_channel.set_permissions(admin_role, send_messages=True)

        # Fetch and post patch notes
        await post_initial_patchnotes(patchnotes_channel)


    # Start checking for new patchnotes
    channel = next((channel for channel in channels_in_category if channel.name == 'cs2-patchnotes'), None)
    await start_patchnote_check(channel)