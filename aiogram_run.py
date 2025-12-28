# aiogram_run.py
import asyncio
from fastapi import FastAPI
from create_bot import bot, dp
from handlers.start import start_router
import uvicorn

app = FastAPI()
dp.include_router(start_router)

@app.get("/")
async def health():
    return {"status": "ok"}

async def start_bot():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    # Создаем задачу для бота
    loop.create_task(start_bot())
    # Запускаем FastAPI через uvicorn (не в отдельном потоке)
    uvicorn.run(app, host="0.0.0.0", port=8080)
