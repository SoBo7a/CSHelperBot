import urllib
import urllib.request
import sqlite3
import asyncio
import json
import os


UPDATE_CYCLE = 4 # Interval (hours) in which we check for new patchnotes
DATABASE_PATH = os.path.join(os.path.dirname(__file__), '../../data/patchnotes.db')


async def fetch_patchnotes_data(appID="730", count="3", maxLength="0", feeds="steam_community_announcements", tags="patchnotes"):
    """
    Fetches patchnotes data from the Steam News API.

    Args:
        appID (str): The application ID for which to fetch news. Default is "730" (Counter Strike).
        count (str): The maximum number of news results to fetch. Default is "3".
        maxLength (str): The maximum length of the news content to fetch. Default is "0" to receive the full length.
        feeds (str): The news feed to fetch from. Default is "steam_community_announcements".
        tags (str): Tags to filter the news results. Default is "patchnotes".

    Returns:
        list: A list of dictionaries containing news items with keys such as 'gid', 'title', 'url', 'is_external_url', 'author', 'contents', 'feedlabel', 'date', 'feedname', 'feed_type', 'appid', and 'tags'.
    """
    url = f"http://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid={appID}&count={count}&maxlength={maxLength}&format=json&feeds={feeds}&tags={tags}"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
    return data.get('appnews', {}).get('newsitems', [])


async def post_content(channel, title, url, contents):
    """
    Posts content to a Discord channel, ensuring that the message length stays within Discord's limit.

    Args:
        channel (discord.TextChannel): The Discord channel where the content will be posted.
        title (str): The title of the message.
        url (str): The URL associated with the message.
        contents (str): The content to be posted, which will be split into multiple messages if it exceeds the length limit.

    Returns:
        None
    """
    contents = contents.replace("[list]", "").replace("[/list]", "")
    contents = contents.replace("[i]", "").replace("[/i]", "")
    contents = contents.replace("[*]", "•")
    
    message_limit = 2000  # Discord message limit
    
    initial_message = f"# {title}\n<{url}>\n"
    initial_message_length = len(initial_message) + 6  # Account for the length of the code block delimiters
    
    # Function to split the content to stay within the message limit
    def split_content(content, limit):
        parts = []
        while len(content) > limit:
            # Find the last newline within the limit
            split_point = content.rfind('\n', 0, limit)
            if split_point == -1:
                # If no newline is found, split at the limit
                split_point = limit
            parts.append(content[:split_point])
            content = content[split_point:].lstrip('\n')  # Remove the newline at the start of the next chunk
        parts.append(content)
        return parts
    
    # Split the contents into chunks that fit within the message limit
    chunks = split_content(contents, message_limit - initial_message_length)
    
    # Send the initial message
    await channel.send(initial_message + f"```{chunks[0]}```")
    
    # Send the remaining chunks
    for chunk in chunks[1:]:
        await channel.send(f"```{chunk}```")
    

async def post_initial_patchnotes(channel):
    """
    Posts initial patch notes about Counter-Strike 2 to the specified Discord channel. It fetches the patch notes,
    identifies the first patch note about CS2, and posts that note and all newer notes to the channel.

    Args:
        channel (discord.TextChannel): The Discord channel where the patch notes will be posted.

    Returns:
        None
    """
    news_items = await fetch_patchnotes_data(count="9999")
    
    index_of_gid = None
    for i, item in enumerate(news_items):
        if item.get('gid') == "5220291886484673985": # gid of the first patchnotes about CS2
            index_of_gid = i
            break
    
    if index_of_gid is not None:
        # Include the CS2 changelog with the specified gid and newer ones
        cs2_patchnotes = news_items[:index_of_gid +1 ]
    else:
        cs2_patchnotes = []
    
    
    for item in reversed(cs2_patchnotes):
        title = item.get('title')
        contents = item.get('contents')
        url = item.get('url')
        date = item.get('date')
        
        await post_content(channel, title, url, contents)
        
    # Initialize database
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS patchnotes
                (title TEXT, date INTEGER)''')
        cursor.execute('''INSERT INTO patchnotes (title, date) VALUES (?, ?)''', (title, date))
        conn.commit()
    

# Function to fetch and post new patchnotes
async def update_patchnotes(channel):
    """
    Fetches the latest patch notes and posts any new ones to the specified Discord channel. The function
    checks the latest patch note date stored in the database and only posts patch notes that are newer.

    Args:
        channel (discord.TextChannel): The Discord channel where the new patch notes will be posted.

    Returns:
        None
    """
    news_items = await fetch_patchnotes_data(count="10")
    
    # Check if there are any new patchnotes
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        latest_patchnote_date = cursor.execute('''SELECT date FROM patchnotes ORDER BY date DESC LIMIT 1''').fetchone()
        
    if latest_patchnote_date:
        latest_patchnote_date = latest_patchnote_date[0]
    
    for item in reversed(news_items):
        title = item.get('title')
        patchnote_date = item.get('date')
        
        # If a newer patchnote is found, update the database and post the new patchnote
        if not latest_patchnote_date or patchnote_date > latest_patchnote_date:
            contents = item.get('contents')
            url = item.get('url')
            
            await post_content(channel, title, url, contents)
            
            # Update the existing entry in the database with the latest patchnote date
            with sqlite3.connect(DATABASE_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute('''DELETE FROM patchnotes''')
                cursor.execute('''INSERT INTO patchnotes (title, date) VALUES (?, ?)''', (title, patchnote_date))
                conn.commit()
            
            return
                        

async def check_for_new_patchnotes(channel):
    """
    Periodically checks for new patch notes and posts any new ones to the specified Discord channel.
    This function runs indefinitely, checking for new patch notes every 3 hours.

    Args:
        channel (discord.TextChannel): The Discord channel where the new patch notes will be posted.

    Returns:
        None
    """
    while True:
        await update_patchnotes(channel)
        await asyncio.sleep(UPDATE_CYCLE * 60 * 60)  # Update every X hours
        

async def start_patchnote_check(channel):
    """
    Starts the periodic patchnote check when the bot starts up by creating an asynchronous task
    that runs the check_for_new_patchnotes function.

    Args:
        channel (discord.TextChannel): The Discord channel where the new patch notes will be posted.

    Returns:
        None
    """
    asyncio.create_task(check_for_new_patchnotes(channel))
