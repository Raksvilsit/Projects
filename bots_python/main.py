 #Импортируем нужные модули
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import aiohttp
from dotenv import load_dotenv
import os
from handlers import function
from aiohttp import web


# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем токены из .env
key = os.getenv('FBOT_TOKEN')
dog = os.getenv('DOG_TOKEN')
cats = os.getenv('CATS_TOKEN')
wea = os.getenv("WEA_TOKEN")

# Создаём экземпляры бота и диспетчера
bot = Bot(token=key)
dp=Dispatcher()
dp.include_router(function.router)

# Функция для очистки апдейтов (чтобы старые сообщения не мешали при запуске бота)
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
            print("бот запущен")

# Главная функция запуска бота
async def main():
    try:
        print("Перед запуском бота очищаем очередь апдейтов...")
        await clear_updates()
    except KeyboardInterrupt:
        print("Бот остановлен вручную")
    finally:
        await bot.session.close()

    # Запускаем диспетчер (бот начинает обрабатывать сообщения)
    await dp.start_polling(bot)

# Запуск бота
if __name__ == "__main__":
    asyncio.run(main()) 



   # 👇 Объявляем хендлер — то, что будет возвращать "I'm alive!"
async def handle(request):
    return web.Response(text="I'm alive!")

# 👇 Создаём приложение и добавляем маршрут /
app = web.Application()
app.add_routes([web.get('/', handle)])

# 👇 Получаем порт от Render или используем 8000 по умолчанию
port = int(os.environ.get("PORT", 8000))

# 👇 Запускаем сервер
web.run_app(app, port=port)







     
