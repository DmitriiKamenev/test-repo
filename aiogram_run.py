# aiogram_run.py
import asyncio
from fastapi import FastAPI
from create_bot import bot, dp
from handlers.start import start_router

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Запускаем бота как background task
    asyncio.create_task(start_bot())

@app.get("/")
async def health():
    return {"status": "ok"}

async def start_bot():
    dp.include_router(start_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
