import asyncio
from fastapi import FastAPI
from create_bot import bot, dp
from handlers.start import start_router
import uvicorn

app = FastAPI()

@app.get("/")
async def health():
    return {"status": "ok"}

async def main():
    dp.include_router(start_router)
    # Запускаем бота в фоне
    asyncio.create_task(dp.start_polling(bot))
    # Запускаем FastAPI
    config = uvicorn.Config(app, host="0.0.0.0", port=8080, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
