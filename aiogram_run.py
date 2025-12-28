import asyncio
from fastapi import FastAPI
from create_bot import bot, dp
from handlers.start import start_router
import uvicorn
import signal
import sys

app = FastAPI()
dp.include_router(start_router)

# Глобальная переменная для сервера Uvicorn
uvicorn_server = None

@app.get("/")
async def health():
    return {"status": "ok"}

@app.post("/shutdown")
async def shutdown_service():
    """Останавливает FastAPI и бота"""
    # Остановка бота
    await bot.close()
    await dp.storage.close()
    await dp.storage.wait_closed()

    # Остановка сервера Uvicorn
    if uvicorn_server:
        uvicorn_server.should_exit = True

    return {"status": "shutting down"}

async def start_bot():
    """Запуск бота в фоне"""
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

async def main():
    global uvicorn_server
    # Запуск бота в фоне
    asyncio.create_task(start_bot())

    # Настройка и запуск FastAPI
    config = uvicorn.Config(app, host="0.0.0.0", port=8080, log_level="info")
    uvicorn_server = uvicorn.Server(config)
    await uvicorn_server.serve()

if __name__ == "__main__":
    # Запуск всего через asyncio.run
    asyncio.run(main())
