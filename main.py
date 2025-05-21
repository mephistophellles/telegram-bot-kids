import asyncio
import os
import logging
from aiogram import Dispatcher, Bot, types
from dotenv import load_dotenv
from app.handlers import router
from aiogram.utils.chat_action import ChatActionMiddleware
from app.database.models import async_main
load_dotenv()
bot = Bot(token=os.getenv("TG_BOT_TOKEN"))

dp = Dispatcher()

async def main():
    await async_main()
    dp.include_router(router)
    dp.message.middleware(ChatActionMiddleware())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')