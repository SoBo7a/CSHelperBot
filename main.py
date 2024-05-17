from bot.bot import setup_bot
import config.settings as settings

def main() -> None:
    bot = setup_bot()
    bot.run(settings.TOKEN)

if __name__ == '__main__':
    main()
