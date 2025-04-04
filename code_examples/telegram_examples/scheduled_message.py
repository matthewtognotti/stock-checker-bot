import asyncio
from telegram import Bot
from .. import constants
from datetime import datetime, timedelta
TELEGRAM_TOKEN = constants.TELEGRAM_TOKEN
TELEGRAM_CHAT_ID = constants.TELEGRAM_CHAT_ID

MESSAGE = "Hello! This is your bot. Sending you a Scheduled Message"


def get_seconds_until(target_hour, target_minute=0):
    now = datetime.now()
    target_time = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
    if target_time < now:
        target_time += timedelta(days=1)
    return (target_time - now).total_seconds()

# Calculate the delay until 4 PM
delay_seconds = get_seconds_until(16)

# Schedule the message
await asyncio.sleep(delay_seconds)

async def main():
    bot = Bot(token=TELEGRAM_TOKEN)
    # Await the coroutine to properly send the message
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=MESSAGE)

if __name__ == '__main__':
    asyncio.run(main())
