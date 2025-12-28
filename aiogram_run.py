import asyncio
from fastapi import FastAPI
from create_bot import bot, dp
from handlers.start import start_router
import uvicorn

app = FastAPI()

@app.get("/")
async def health():
    return {"status": "ok"}

async def start_bot_task():
    dp.include_router(start_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    dp.include_router(start_router)
    loop = asyncio.get_event_loop()
    # Запускаем бота в фоне
    loop.create_task(start_bot_task())
    # Запускаем FastAPI в основном процессе
    uvicorn.run(app, host="0.0.0.0", port=8080)
