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

def main():
    # uvicorn.run сам блокирует поток, но мы можем использовать on_startup
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="info",
        loop="asyncio",
        reload=False,
        factory=False,
        access_log=False,
        lifespan="on",
        on_startup=[start_bot]  # запускаем бота после старта сервера
    )

if __name__ == "__main__":
    main()
