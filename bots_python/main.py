from aiogram import Bot, Dispatcher
from aiogram.filters import Command
import asyncio
import aiohttp
from aiohttp import web
from dotenv import load_dotenv
import os

from handlers import function

load_dotenv()

# Получаем токены из .env
key = os.getenv('FBOT_TOKEN')

# Создаем бота и диспетчер
bot = Bot(token=key)
dp = Dispatcher()
dp.include_router(function.router)

# Очистка апдейтов
async def clear_updates():
    url = f"https://api.telegram.org/bot{key}/getUpdates"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            print("Ответ API:", data)
        if data.get("result"):
            last_update_id = data["result"][-1]["update_id"]
            await session.get(f"{url}?offset={last_update_id + 1}")
            print(f"Очистил апдейты до update_id={last_update_id}")
        else:
            print("Нет новых апдейтов")

# Aiohttp обработчик
async def handle(request):
    return web.Response(text="I'm alive!")

# Главная функция
async def on_startup(app):
    await clear_updates()
    asyncio.create_task(dp.start_polling(bot))

# Создание aiohttp-приложения
app = web.Application()
app.router.add_get("/", handle)
app.on_startup.append(on_startup)

# Запуск
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    web.run_app(app, port=port)







     
