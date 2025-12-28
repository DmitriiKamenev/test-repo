import asyncio
from fastapi import FastAPI
from create_bot import bot, dp, scheduler
from handlers.start import start_router
import uvicorn

# --- FastAPI ---
app = FastAPI()
dp.include_router(start_router)

@app.get("/")
async def health():
    return {"status": "ok"}

# --- функция старта бота ---
async def start_bot():
    await bot.delete_webhook(drop_pending_updates=True)
    # Запуск polling в фоне, чтобы не блокировать uvicorn
    asyncio.create_task(dp.start_polling(bot))

if __name__ == "__main__":
    # uvicorn держит основной процесс живым и слушает порт 8080
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="info",
        on_startup=[start_bot]  # бот стартует после поднятия сервера
    )
