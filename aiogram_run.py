import asyncio
from fastapi import FastAPI
from create_bot import bot, dp
from handlers.start import start_router
from routers.build import router
from handlers.callback_handlers import callback_router
import uvicorn

app = FastAPI()
dp.include_router(start_router)
dp.include_router(router)
dp.include_router(callback_router)


bot_task: asyncio.Task | None = None

@app.get("/")
async def health():
    return {"status": "ok"}

async def start_bot():
    """Запуск polling бота"""
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

async def main():
    global bot_task
    bot_task = asyncio.create_task(start_bot())

    # Запуск FastAPI через Uvicorn
    config = uvicorn.Config(app, host="0.0.0.0", port=8080, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
