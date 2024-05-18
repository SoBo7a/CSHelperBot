from dotenv import dotenv_values

config = dotenv_values(".env")
TOKEN = config.get('TOKEN')
STEAM_API_KEY = config.get('STEAM_API_KEY')


if not TOKEN:
    raise ValueError("No TOKEN found in environment variables. Make sure to set it in the .env file.")

if not STEAM_API_KEY:
    raise ValueError("No STEAM_API_KEY found in environment variables. Make sure to set it in the .env file.")