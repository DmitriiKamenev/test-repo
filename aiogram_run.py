import asyncio
from fastapi import FastAPI
import threading
from create_bot import bot, dp, scheduler
from handlers.start import start_router

# --- FastAPI для health check ---
app = FastAPI()

@app.get("/")
async def health():
    return {"status": "ok"}

def start_fastapi():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

# --- aiogram бот ---
async def start_bot():
    dp.include_router(start_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

def main():
    # запускаем FastAPI в отдельном потоке
    threading.Thread(target=start_fastapi, daemon=True).start()
    # запускаем бота
    asyncio.run(start_bot())

if __name__ == "__main__":
    main()
