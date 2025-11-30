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
        'Clouds': 'Облачно',
        'Clear': 'Чисто',
        'Few clouds': 'Небольшая облачность',
        'Scattered clouds': 'Переменная облачность',
        'Broken clouds': 'Разорванная облачность',
        'Overcast': 'Пасмурно',
        'Rain': 'Дождь',
        'Drizzle': 'Морось',
        'Thunderstorm': 'Гроза',
        'Snow': 'Снег',
        'Mist': 'Туман',
        'Fog': 'Сильный туман'
    }
    description = weather_descriptions.get(weather, "Неопределённая погода")
    return f"Погода в {user_input}: {description}\nТемпература в {user_input} {temp_celsius}ºC"

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Здравствуйте !\nНапишите название города, и я предоставлю вам информацию о погоде.")

@dp.message_handler()
async def handle_message(message: types.Message):
    user_input = message.text
    weather_info = get_weather(user_input)
    await message.reply(weather_info)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
