import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <-- добавили
from create_bot import bot, dp
from handlers.start import start_router
import uvicorn

app = FastAPI()
dp.include_router(start_router)

# ----------- Настройка CORS -----------
origins = [
    "*"  # разрешаем все источники, можно указать конкретные фронтенды
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # разрешаем все методы, включая OPTIONS
    allow_headers=["*"],
)
# --------------------------------------

bot_task: asyncio.Task | None = None

@app.get("/")
async def health():
    return {"status": "ok"}

@app.post("/shutdown")
async def shutdown_service():
    global bot_task
    try:
        if bot_task and not bot_task.done():
            bot_task.cancel()
            try:
                await bot_task
            except asyncio.CancelledError:
                pass

        if dp.storage:
            await dp.storage.close()

        if bot.session:
            await bot.session.close()

        return {"status": "bot stopped"}

    except Exception as e:
        return {"status": "error", "detail": str(e)}

async def start_bot():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

async def main():
    global bot_task
    bot_task = asyncio.create_task(start_bot())
    config = uvicorn.Config(app, host="0.0.0.0", port=8080, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
