## v1.0.7
[FIXES]
- Fixed issue with vac-watcher, where false positives were generated
- Updated Readme
- Updated translation for vac-watcher channel description

## v1.0.6
[FEATURES]
- Added the /vac_check command, allowing users to monitor SteamIDs for 360 days and receive notifications if any of the monitored SteamIDs are VAC banned.

[IMPROVEMENTS]
- code refactoring
- updated instructions channel with the latest changes
- cooldown for /teams allows now 5 commands every 30 minutes

## v1.0.5
[IMPROVEMENTS]
- /stats: best map in stats is now based on win-rates and average rounds on each map
- GUILD_ID is now stored in .env

## v1.0.4
[IMPROVEMENTS]
- /stats now shows the steam username and as a link to the profile instead of the discord mention
- /stats now has an "user" option that allows to give any steamID and check the stats for it

## v1.0.3
[FEATURES]
- Implemented a new channel named "cs2-patchnotes" within the bot's category to display recent and upcoming CS2 patch note

[FIXES]
- Resolved issue where users receive no error messages if /stats returns a 403 Forbidden status, typically due to Steam privacy settings.

[MISC]
- code refactoring
- implemented basic logging

## v1.0.2
- added multi language support (english and german)

## v1.0.1
- some code refactoring
- 3 minute cooldown for /stats
- now automatically creates its own category with a "instructions" and "commands" textchannel when first joining a server

## v1.0.0
- initial release