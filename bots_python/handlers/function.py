from aiogram import types, F
from aiogram.filters import Command
from aiogram import Router
import aiohttp
import dotenv
import asyncio
from dotenv import load_dotenv
import os
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

load_dotenv()


cats = os.getenv('CATS_TOKEN')
dog = os.getenv('DOG_TOKEN')
key = os.getenv('FBOT_TOKEN')

router = Router()

wea = os.getenv("WEA_TOKEN")


# FSM 
class WeatherStates(StatesGroup):
    waiting_location = State()

async def get_weather(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": wea,
        "units": "metric",
        "lang": "ru"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            if resp.status == 200:
                data = await resp.json()
                city = data.get("name")
                temp = data["main"]["temp"]
                feels = data["main"]["feels_like"]
                humidity = data["main"]["humidity"]
                pressure = data["main"]["pressure"]
                wind_speed = data["wind"]["speed"]
                wind_speed_kmh = round(wind_speed * 3.6, 1)
                description = data["weather"][0]["description"]

                result = (
                    f"🌍 Город: {city}\n"
                    f"🌡 Температура: {temp}°C (ощущается как {feels}°C)\n"
                    f"💧 Влажность: {humidity}%\n"
                    f"🌀 Давление: {pressure} гПа\n"
                    f"💨 Ветер: {wind_speed} м/с (~{wind_speed_kmh} км/ч)\n"
                    f"☁️ {description.capitalize()}"
                )
                return result
            else:
                return f"Ошибка {resp.status}: не удалось получить данные о погоде."

# /weather: запрос геолокации 
@router.message(Command(commands=["weather"]))
async def weather_start(message: types.Message, state: FSMContext):
    button = types.KeyboardButton(text="Отправить геолокацию", request_location=True)
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[button]],
        resize_keyboard=True
    )
    await message.answer(
        "Пожалуйста, отправьте свою геолокацию для просмотра погоды.\n"
        "Если не хотите, отправьте любое сообщение без геолокации.",
        reply_markup=keyboard
    )
    await state.set_state(WeatherStates.waiting_location)

#Получение геолокации 
@router.message(WeatherStates.waiting_location, F.content_type == "location")
async def location_received(message: types.Message, state: FSMContext):
    lat = message.location.latitude
    lon = message.location.longitude
    weather_info = await get_weather(lat, lon)
    await message.answer(weather_info, reply_markup=types.ReplyKeyboardRemove())
    await state.clear()


@router.message(WeatherStates.waiting_location)
async def location_not_received(message: types.Message, state: FSMContext):
    # Координаты по умолчанию (например, твои)
    lat = 53.198627
    lon = 50.113987
    weather_info = await get_weather(lat, lon)
    await message.answer(
        "Геолокация не получена. Вот погода по умолчанию:", reply_markup=types.ReplyKeyboardRemove()
    )
    await message.answer(weather_info)
    await state.clear()



@router.message(Command(commands=["cats"]))
async def send_cat(message: types.Message):
    await message.answer("Случайное фото кота...")
    url = "https://api.thecatapi.com/v1/images/search"
    headers = {"x-api-key": cats}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                image_url = data[0]["url"]
                await message.answer_photo(image_url)
            else:
                await message.answer("Ошибка при получении кота.")

@router.message(Command(commands=["dog"]))
async def send_dog(message: types.Message):
    await message.answer("Случайное фото собаки...")
    url = "https://api.thedogapi.com/v1/images/search"
    headers = {"x-api-key": dog}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                image_url = data[0]["url"]
                await message.answer_photo(image_url)
            else:
                await message.answer("Ошибка при получении собаки.")

@router.message(Command(commands=["start"]))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот, созданный с помощью библиотеки aiogram")

@router.message(Command(commands=["info"]))
async def info_handler(message: types.Message):
    await message.answer("Информация о боте ")



