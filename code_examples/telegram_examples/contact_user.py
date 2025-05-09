import asyncio
from telegram import Bot
from dotenv import load_dotenv
from os import getenv

# Load environment variables from the .env file
load_dotenv()

TELEGRAM_TOKEN = getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = getenv("TELEGRAM_CHAT_ID")
MESSAGE = "Hello! This is your bot."


async def main():
    bot = Bot(token=TELEGRAM_TOKEN)
    # Await the coroutine to properly send the message
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=MESSAGE)


if __name__ == "__main__":
    asyncio.run(main())
