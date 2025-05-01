import os
from aiogram import Dispatcher, Bot, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import asyncio

from dotenv import load_dotenv, find_dotenv

from common.bot_cmd_list import private
from handlers.user_private import user_private_router

load_dotenv(find_dotenv())
bot = Bot(token=os.getenv("TOKEN"), defaults=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


dp.include_router(user_private_router)

async def on_startup(bot):
    print("бот заработал!")

async def on_shutdown(bot):
    print("бот лёг отдохнуть...")


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())



