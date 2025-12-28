import asyncio
from create_bot import bot, dp, scheduler
from handlers.start import start_router
from fastapi import FastAPI
import uvicorn

# Настраиваем HTTP сервер для health check
app = FastAPI()


@app.get("/")
async def health():
    return {"status": "ok"}


async def start_bot():
    # dp.include_router(start_router) нужно делать здесь
    dp.include_router(start_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def main():
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()
    bot_task = asyncio.create_task(start_bot())

    # uvicorn.run блокирует поток, поэтому запускаем его как задачу в asyncio
    config = uvicorn.Config(app, host="0.0.0.0", port=8080, log_level="info")
    server = uvicorn.Server(config)
    server_task = asyncio.create_task(server.serve())

    # Ждём пока обе задачи работают
    await asyncio.gather(bot_task, server_task)


if __name__ == "__main__":
    asyncio.run(main())
