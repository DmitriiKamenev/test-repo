import asyncio
from fastapi import FastAPI
from create_bot import bot, dp
from handlers.start import start_router
import uvicorn

# FastAPI для health check
app = FastAPI()

@app.get("/")
async def health():
    return {"status": "ok"}

# Aiogram бот
async def start_bot():
    dp.include_router(start_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

async def main():
    # запускаем FastAPI и бота параллельно
    config = uvicorn.Config(app, host="0.0.0.0", port=8080, log_level="info")
    server = uvicorn.Server(config)

    # два короутина одновременно
    await asyncio.gather(
        server.serve(),   # FastAPI
        start_bot()       # Aiogram бот
    )

if __name__ == "__main__":
    asyncio.run(main())
