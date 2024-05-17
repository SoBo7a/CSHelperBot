from dotenv import dotenv_values

config = dotenv_values(".env")
TOKEN = config.get('TOKEN')

if not TOKEN:
    raise ValueError("No TOKEN found in environment variables. Make sure to set it in the .env file.")
