import db # файл с работой с базой данных
import config # файл с токенами
import datetime # для работы с временем
import telebot # для работы с телеграм ботом
import requests # модуль для запросов
from geopy import geocoders # модуль для определение координат населенного пункта


# Функция для получения данных о погоде по координатам
def get_weather(lat, lon):
    r = requests.get(f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={config.token_open_weather}&units=metric&lang=ru')
    data = r.json()
    return data


# Функция определяет широту населенного пункта
def geo_pos(city: str):
    geolocator = geocoders.Nominatim(user_agent="telebot")
    latitude = str(geolocator.geocode(city).latitude)
    return latitude


# Функция определяет долготу населенного пункта
def geo_pos_1(city: str):
    geolocator = geocoders.Nominatim(user_agent="telebot")
    longitude = str(geolocator.geocode(city).longitude)
    return longitude


# Функция вывода нужных нам данных
def print_weather(data):
    city = data["name"]
    cur_weathers = data['main']['temp']
    humidity = data['main']['humidity']
    pressure = data['main']['pressure']
    wind = data['wind']['speed']
    weather_descriptions = data['weather'][0]['description']
    sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
    sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])
    length_of_the_day = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(data['sys']['sunrise'])
    return f'Погода в городе {city} на дату {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\n' \
           f'Температура - {cur_weathers} С°\n' \
           f'Влажность - {humidity}\n' \
           f'Скорость ветра - {wind} м/с\n' \
           f'Давление - {pressure} мм.рт.ст\n' \
           f'Погода - {weather_descriptions}\n' \
           f'Восход солнца - {sunrise}\n' \
           f'Заход солнца - {sunset}\n' \
           f'Длительность дня - {length_of_the_day}\n' \
           f'Хорошего дня.\n' \
           f'https://yandex.by/pogoda/?lat={geo_pos(city)}&lon={geo_pos_1(city)}'


bot = telebot.TeleBot(config.token)


# Декораток, если в пользователь ввел команду /start срабатывает функция start с выводом на экран приветственного сообщения
# Функция так же проверяет первый раз ли пользователь использует бота, если первый то добавляет ид пользователя в БД
@bot.message_handler(commands=["start"])
def start(message):
    if db.users(message.from_user.id) == True: # проверяет есть ли ид пользователя в БД
        bot.send_message(message.from_user.id, f'Рады сного видеть вас {message.from_user.first_name}!\n'
                                            'Это информационный бот по Островецкому району, Республики Беларусь.\n'
                                            'Здесь ты можешь задать вопрос из списка /ask и получить на него ответ.\n'
                                            'Так же можешь совершить действия узнав погоду в городе командой "Погода".\n'
                                            'Удачи в пользовании!')
    else:
        print(message.from_user.id)
        db.add_user(message.from_user.id)
        bot.send_message(message.from_user.id, f'Приветствуем нового пользователя, {message.from_user.first_name}!\n'
                                            'Это информационный бот по Островецкому району, Республики Беларусь.\n'
                                            'Здесь ты можешь задать вопрос из списка /ask и получить на него ответ.\n'
                                            'Так же можешь совершить действия узнав погоду в '
                                               'городе командой "Погода".\n'
                                            'Удачи в пользовании!')


# Декорато, принимает текст и передает его в фукция get_text_messages
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/ask" or message.text == ".фыл":
        bot.send_message(message.from_user.id, db.info_ask()) # вызывает функцию из файла db для возвращения списка доступных вопросов
    elif message.text == '/help' or message.text == ".рудз": # повторно выводит описание бота и его возможностей
        bot.send_message(message.from_user.id,
                         f'{message.from_user.first_name}! Это информационный бот по Островецкому району, Республики Беларусь.\n'
                         'Здесь ты можешь задать вопрос из списка /ask и получить на него ответ.\n'
                         'Так же можешь совершить действия узнав погоду в городе командой "Погода".\n'
                         'Удачи в пользовании!')
    # проверяет есть ли заданный вопрос в базе данных
    elif message.text.lower() in db.ask():
        # выводит ответ для заданного вопроса
        bot.send_message(message.from_user.id, db.ask_answer(message.text))
    elif message.text == 'Погода' or message.text == 'погода':
        city = 'Островец'
        # вызывает функцию вывода данных о погоде
        bot.send_message(message.from_user.id, print_weather(get_weather(geo_pos(city), geo_pos_1(city))))
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


bot.polling(none_stop=True)
