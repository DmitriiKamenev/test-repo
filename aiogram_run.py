import asyncio
from fastapi import FastAPI
from create_bot import bot, dp
from handlers.start import start_router
import uvicorn

app = FastAPI()
dp.include_router(start_router)

bot_task: asyncio.Task | None = None

@app.get("/")
async def health():
    return {"status": "ok"}

@app.post("/shutdown")
async def shutdown_service():
    """Останавливаем бота безопасно на Back4App"""
    global bot_task

    try:
        if bot_task and not bot_task.done():
            bot_task.cancel()
            try:
                await bot_task
            except asyncio.CancelledError:
                pass

        # Закрытие storage и сессии бота
        if dp.storage:
            await dp.storage.close()

        if bot.session:
            await bot.session.close()

        return {"status": "bot stopped"}

    except Exception as e:
        return {"status": "error", "detail": str(e)}

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
