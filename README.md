# CS Helper Bot
Discord CS Helper Bot is a Discord bot designed to manage and facilitate CS2 play sessions. It allows users to subscribe to notifications for when others want to play, create and move teams into voice channels, enables you to see you CS2 stats and handles other related tasks.

## Features
- Play Notifications: Users can subscribe to receive notifications when someone wants to play CS2.
- Team Management: Randomly move users into teams within designated voice channels.
- Stats Tracking: Retrieve CS2 player statistics from Steam.
- Random Map: Get a random Map out of a list of all CS2 Maps. You can get either Standard or Wingman Maps.
- Creates a new category in the channel dedicated to the bot, which includes:
    - A tutorial channel to provide guidance on utilizing the bot.
    - A commands channel dedicated to using bot commands without cluttering other channels.
    - A cs2-patchnotes channel designed to display all past and forthcoming patch notes related to CS2.

## Setup and Installation
1. Clone the repository:
```bash
git clone https://github.com/SoBo7a/CSHelperBot.git
cd CSHelperBot
```

2. Create and activate a virtual environment (for Windows):
```bash
python -m venv venv
./venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Configure the bot:
- Create a .env file in the root directory of the project.
- Add your bot token and other necessary configurations:
```
TOKEN = YOUR_DISCORD_BOT_TOKEN
STEAM_API_KEY = YOUR_STEAM_API_KEY
GUILD_ID = YOUR_GUILD_ID
```
- Set your desired Language in the config.json ("de" for German or "en" for English):
```json
{
    "language": "en"
}
```

6. Create the databases:
- Create a folder called "data" in the root directory of the project.
- Create the "vac_check.db", "patchnotes.db", "play.db" and "stats.db" files in the "data" directory

7. Run the bot:
```bash
python main.py
```

8. Setup Voice channels on your Discord server:
- Create the following voice channels, for /teams command to work:
    - CS2
    - Terrorists
    - Anti Terrorists

## Commands

### /play
- Description: Notify users that you want to play CS2 or manage your subscription to play notifications.
- Usage:
```
/play [action]
```
- Parameters:
    - action (optional): Choose subscribe to subscribe or unsubscribe to unsubscribe from play notifications.

### /teams
- Description: Creates and moves users to teams.
- Usage:
```
/teams
```
- End Session: End the current session by using the button and move all users back to the 'CS2' voice channel.
- Permissions: Only accessible to users with administrator permissions.
- Requirements:
    - The command must be used in the text channel corresponding to the 'CS2' voice channel.
    - The user must be in the 'CS2' voice channel when using the command.

### /map
- Description: Selects a random CS2 map from the specified map pool.
- Usage:
```
/map [mode]
```
- Parameters:
    - "mode" (optional): Choose between standard for the standard map pool or wingman for the Wingman map pool. Defaults to standard if not specified.
- Example:
    - /map standard: Selects a random map from the standard CS2 map pool.
    - /map wingman: Selects a random map from the Wingman map pool.

### /stats
- Description: Manage your CS2 stats by setting up your Steam ID or retrieving and displaying your CS2 statistics.
- Usage:
```
/stats [setup_steamid] or [user]
```
- Features:
    - Setup Steam ID: Use /stats steamid YOUR_STEAM_ID to set up your Steam ID.
    - Retrieve Stats: If no Steam ID is provided, it will fetch and display the stats for the stored Steam ID.
- Displayed Stats:
    - Total Time Played (Hours): Total hours spent playing CS2.
    - Best Map: The map with the highest number of wins.
    - Best Weapon: The weapon with the highest number of kills.
    - Total Kills: Total number of kills.
    - Total Deaths: Total number of deaths.
    - KD Ratio: Kill-to-death ratio.
    - Total Matches Won: Total number of matches won.
    - Total Matches Played: Total number of matches played.
    - Win Rate: Win rate percentage based on total matches won and played.
- Example:
    - /stats setup_steamid 1234567890: Sets up the Steam ID 1234567890 for the user.
    - /stats: Retrieves and displays the stored stats for the user.
    - /stats user 1234567890: recieves the stats for the given Steam ID.

### /vac_check
- Description: Check VAC ban status for a given Steam ID and monitor it for 360 days.
- Usage:
```
/vac_check [SteamID]
```
- Parameters:
    - SteamID: The Steam ID to check for VAC bans and monitor.
- Features:
    - Monitors the specified Steam ID for 360 days.
    - Notifies users if the monitored Steam ID gets VAC banned.
- Example:
    - /vac_check 1234567890: Checks the VAC ban status for the Steam ID 1234567890 and monitors it for 360 days.

## License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/SoBo7a/CSHelperBot/blob/main/LICENSE.md) file for more details.

## Acknowledgements
- [discord.py](https://github.com/Rapptz/discord.py) - An API wrapper for Discord written in Python.
- CSButler logo - The logo for the Bot created by [SonZza](https://x.com/SonZza4Real).