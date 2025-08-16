import os
import sys
import logging
import asyncio

from aiogram import Bot, Dispatcher, types
from aiohttp import web
from dotenv import load_dotenv

from app.handlers.router import admin_router, user_router
from app.middlewares.antiflud import ThrottlingMiddleware

load_dotenv()

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Empty bot token given")

WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}{WEBHOOK_PATH}"
PORT = int(os.getenv("PORT", 8000))


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def main() -> None:
    dp.message.middleware(ThrottlingMiddleware(limit=0.5))
    dp.include_router(admin_router)
    dp.include_router(user_router)
    dp.startup.register(on_startup)
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, webhook_handler)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    web.run_app(app, port=PORT)

async def webhook_handler(request):
    logging.info("Incoming webhook hit")
    update = types.Update(**await request.json())
    await dp.feed_update(update=update, bot=bot)
    return web.Response(text="OK")

async def on_startup(app: web.Application):
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"Webhook set to {WEBHOOK_URL}")

async def on_shutdown(app: web.Application):
    logging.info("Shutting down...")
    await bot.session.close()
    await bot.delete_webhook()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    main()