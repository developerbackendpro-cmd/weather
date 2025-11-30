import requests
from aiogram.utils import executor
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware

API_KEY = '30d4741c779ba94c470ca1f63045390a'
BOT_TOKEN = ''

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

def get_weather(user_input):
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=imperial&APPID={API_KEY}")
    data = response.json()
    if data['cod'] == '404':
        return "Hech qanday shahar topilmadi"
    weather = data['weather'][0]['main']
    temp_fahrenheit = round(data['main']['temp'])
    temp_celsius = round((temp_fahrenheit - 32) * 5 / 9)
    weather_descriptions = {
        'Clouds': 'Bulutli',
        'Clear': 'Toza',
        'Few clouds': 'Kam bulutli',
        'Scattered clouds': 'Tarqalgan bulutlar',
        'Broken clouds': 'Yoyilgan bulutlar',
        'Overcast': 'Bulutli',
        'Rain': 'Yomg\'ir',
        'Drizzle': 'Yog\'ingarchilik',
        'Thunderstorm': 'Momaqaldiroq',
        'Snow': 'Qor',
        'Mist': 'Tuman',
        'Fog': 'Kuchli Tuman'
    }
    description = weather_descriptions.get(weather, "Bilinmaydigan ob-havo")
    return f"Ob-havo {user_input}da {description}\nHarorat {user_input}da {temp_celsius}ºC"

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Salom! Shaharning nomini yozing va men sizga ob-havo ma'lumotlarini taqdim etaman.")

@dp.message_handler()
async def handle_message(message: types.Message):
    user_input = message.text
    weather_info = get_weather(user_input)
    await message.reply(weather_info)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)