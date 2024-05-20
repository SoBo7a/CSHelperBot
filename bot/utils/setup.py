from discord import Guild, utils, File
import os


base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
empty_line = "\u200B"


async def send_tutorial(instructions_channel):
    # Send the headline
    await instructions_channel.send("**Anleitung zur Nutzung des CS Butler Bots**\n")

    # Feature: /teams
    teams_message = await instructions_channel.send("**Feature 1: /teams**\nMit dem Befehl `/teams` können Administratoren Teams für ein Spiel erstellen. Der Bot wird zufällig zwei Teams aus den anwesenden Spielern zusammenstellen.\nAlle Spieler müssen sich hierzu im CS2 Voice Channel befinden. Der Befehl muss ebenfalls im Chat des Voice Channels eingegeben werden.\nUm die Session zu beenden und die Spieler wieder in den CS2-Chat zu verschieben, kann der 'End Session'-Button verwendet werden.")
    teams_thread = await teams_message.create_thread(name="Feature 1: /teams")
    teams_image_path = os.path.join(base_dir, 'assets', 'img', 'Tutorial_teams.png')
    with open(teams_image_path, 'rb') as f:
        picture = File(f, spoiler=True)
        await teams_thread.send(file=picture)

    # Feature: /play
    play_message = await instructions_channel.send("\n**Feature 2: /play**\nDer Befehl `/play` sendet eine Privatnachricht in Discord an alle Abonnenten, die eine Einladung zum CS2 Voice Channel enthält, um darüber zu informieren, dass jemand CS2 spielen möchte.\nUm die Privatnachrichten zu erhalten, müssen ggf. die Datenschutzeinstellungen in Discord angepasst werden.")
    play_thread = await play_message.create_thread(name="Feature 2: /play")
    await play_thread.send("\n**Abonnieren oder Deabonnieren der /play-Benachrichtigungen:**")
    play_image1 = os.path.join(base_dir, 'assets', 'img', 'Tutorial_play_sub1.png')
    with open(play_image1, 'rb') as f:
        picture = File(f, spoiler=True)
        await play_thread.send(file=picture)
    play_image2 = os.path.join(base_dir, 'assets', 'img', 'Tutorial_play_sub2.png')
    with open(play_image2, 'rb') as f:
        picture = File(f, spoiler=True)
        await play_thread.send(file=picture)
    await play_thread.send("Nun kann zwischen 'Subscribe' und 'Unsubscribe' gewählt werden:")
    play_image3 = os.path.join(base_dir, 'assets', 'img', 'Tutorial_play_sub3.png')
    with open(play_image3, 'rb') as f:
        picture = File(f, spoiler=True)
        await play_thread.send(file=picture)
    await play_thread.send("Anschließend erhält man die Bestätigung des Vorgangs:")
    play_image4 = os.path.join(base_dir, 'assets', 'img', 'Tutorial_play_sub4.png')
    with open(play_image4, 'rb') as f:
        picture = File(f, spoiler=True)
        await play_thread.send(file=picture)
    await play_thread.send("Der `/play`-Befehl kann nun verwendet werden:")
    play_image5 = os.path.join(base_dir, 'assets', 'img', 'Tutorial_play_sub5.png')
    with open(play_image5, 'rb') as f:
        picture = File(f, spoiler=True)
        await play_thread.send(file=picture)

    # Feature: /map
    map_message = await instructions_channel.send("\n**Feature 3: /map**\nDer Befehl `/map` schlägt eine zufällig ausgewählte CS2-Map für Standard- oder Wingman-Spiele vor.")
    map_thread = await map_message.create_thread(name="Feature 3: /map")
    await map_thread.send("Für eine Standard-Map genügt der `/map`-Befehl allein. Um eine Wingman-Map zu erhalten, befolgt bitte die folgenden Schritte:")
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
    stats_message = await instructions_channel.send("\n**Feature 4: /stats**\nDer Befehl `/stats` zeigt die eigene Counter-Strike-Statistik (CSGO + CS2) aus Steam an.")
    stats_thread = await stats_message.create_thread(name="Feature 4: /stats")
    await stats_thread.send("Um den Befehl verwenden zu können, muss zuerst die eigene SteamID gespeichert werden. Die SteamID findet sich im Link zu eurem Profil:")
    stats_image0 = os.path.join(base_dir, 'assets', 'img', 'Tutorial_stats_steamid.png')
    with open(stats_image0, 'rb') as f:
        picture = File(f, spoiler=True)
        await stats_thread.send(file=picture)
    await stats_thread.send("Das Steamprofil muss bestimmte Datenschutzeinstellungen haben, damit die Statistiken für den Bot zugänglich sind (Statistiken sind erst einige Minuten nach dem Ändern der Einstellungen abrufbar):")
    stats_image1 = os.path.join(base_dir, 'assets', 'img', 'Tutorial_stats_steamid1.png')
    with open(stats_image1, 'rb') as f:
        picture = File(f, spoiler=True)
        await stats_thread.send(file=picture)
    await stats_thread.send("Eure SteamID muss nun mit dem Befehl `/stats steamid 1234567890` mit dem Discord-Konto verknüpft werden.:")
    stats_image2 = os.path.join(base_dir, 'assets', 'img', 'Tutorial_stats_steamid2.png')
    with open(stats_image2, 'rb') as f:
        picture = File(f, spoiler=True)
        await stats_thread.send(file=picture)
    stats_image3 = os.path.join(base_dir, 'assets', 'img', 'Tutorial_stats_steamid3.png')
    with open(stats_image3, 'rb') as f:
        picture = File(f, spoiler=True)
        await stats_thread.send(file=picture)
    await stats_thread.send("Hier bitte die SteamID einfügen:")
    stats_image4 = os.path.join(base_dir, 'assets', 'img', 'Tutorial_stats_steamid4.png')
    with open(stats_image4, 'rb') as f:
        picture = File(f, spoiler=True)
        await stats_thread.send(file=picture)
    stats_image5 = os.path.join(base_dir, 'assets', 'img', 'Tutorial_stats_steamid5.png')
    with open(stats_image5, 'rb') as f:
        picture = File(f, spoiler=True)
        await stats_thread.send(file=picture)
    await stats_thread.send("Der `/stats`-Befehl kann nun verwendet werden:")
    stats_image6 = os.path.join(base_dir, 'assets', 'img', 'Tutorial_stats_steamid6.png')
    with open(stats_image6, 'rb') as f:
        picture = File(f, spoiler=True)
        await stats_thread.send(file=picture)
        
    await instructions_channel.send(empty_line)

    # Conclusion    
    mention = f"<@693204479259967559>"
    github_link = "https://github.com/SoBo7a/CSHelperBot"
    await instructions_channel.send(f"**Für Support, Fehlermeldungen oder Feature-Anfragen, bitta an {mention} wenden. Für weitere Informationen und den Quellcode des Bots besuche {github_link}.**")
    

async def setup_channels(guild: Guild):
    # Check for bot category and create it if it doesn't exist
    category = utils.get(guild.categories, name='CS2-Butler-Bot')
    if not category:
        category = await guild.create_category('CS2-Butler-Bot')
        
        # Set the category's position to be just below the top position
        top_position = guild.categories[0].position
        await category.edit(position=top_position)
        
        # Create the Instructions channel if it doesn't exist
        instructions_channel = utils.get(guild.text_channels, name='Instructions')
        if not instructions_channel:
            instructions_channel = await guild.create_text_channel('Instructions', category=category)
            await instructions_channel.edit(topic='Willkommen zur Anleitung für den CS Butler Bot. Diese Anleitung erklärt die Nutzung des Bots und seine Funktionen.')

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
            await commands_channel.edit(topic='Dieser Kanal ist für Befehle des CS Butler reserviert und verhindert die unnötige Nutzung anderer Textkanäle.')

            # Set channel permissions for Commands channel
            await commands_channel.set_permissions(everyone_role, read_messages=True, send_messages=True)
