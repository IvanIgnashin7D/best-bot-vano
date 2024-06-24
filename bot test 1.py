from telebot import *
from types import *
import requests

token = '7252009265:AAEScH2fMjOI1xQakbhJPM0MDDpkONzhaLs'
bot = TeleBot(token=token)


@bot.message_handler(commands=['start'])
def privet(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=False)
    button1 = types.KeyboardButton(text='Написать сообщение с ссылками')
    button2 = types.KeyboardButton(text='Отправить фото с подписью')
    button3 = types.KeyboardButton(text='Отправить одну ссылку')
    button4 = types.KeyboardButton(text='Отправить всем привет')
    button5 = types.KeyboardButton(text='Рандомное фото')
    button6 = types.KeyboardButton(text='Получить информацию обо мне')
    keyboard.add(button1, button2, button3, button4, button5, button6)
    text = 'Привет, я бот'
    user_id = str(message.chat.id)
    file = open('users.TXT', 'r')
    txt = file.read().split(' ')
    file.close()
    file = open('users.TXT', 'a')
    if user_id not in txt:
        file.write(user_id+' ')
    file.close()
    bot.send_message(message.chat.id, text=text, reply_markup=keyboard)
    with open('logs.TXT', 'a') as logs:
        print(f'Пользователь {message.from_user.first_name} написал "{message.text}', file=logs)
        # print(f'Бот ответил: "{text}"', file=logs)


@bot.message_handler(commands=['ssilki'])
@bot.message_handler(func= lambda message: message.text == 'Написать сообщение с ссылками')
def send_ssilki(message):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text='Vikipedia', url='https://ru.wikipedia.org/wiki/%D0%92%D0%B8%D0%BA%D0%B8%D0%BF%D0%B5%D0%B4%D0%B8%D1%8F')
    button2 = types.InlineKeyboardButton(text='Telegram', url='https://ru.wikipedia.org/wiki/Telegram')
    keyboard.add(button1, button2)
    bot.send_message(message.chat.id, text='Вот кнопки с ссылками:', reply_markup=keyboard)
    with open('logs.TXT', 'a') as logs:
        print(f'Пользователь {message.from_user.first_name} написал "{message.text}', file=logs)


@bot.message_handler(commands=['photo'])
@bot.message_handler(func= lambda message: message.text == 'Отправить фото с подписью')
def send_photo(message):
    photo = open('x_915201e5.jpg', 'rb')
    bot.send_photo(message.chat.id, photo, caption='Вот фото сверху')
    with open('logs.TXT', 'a') as logs:
        print(f'Пользователь {message.from_user.first_name} написал "{message.text}', file=logs)


@bot.message_handler(commands=['ssilka'])
@bot.message_handler(func= lambda message: message.text == 'Отправить одну ссылку')
def send_ssilka(message):
    bot.send_message(message.chat.id, text='Вот ссылка на гугл: https://www.google.ru/')
    with open('logs.TXT', 'a') as logs:
        print(f'Пользователь {message.from_user.first_name} написал "{message.text}', file=logs)


@bot.message_handler(func=lambda message: message.text.lower() == 'отправить всем привет')
def hello_all(message):
    txt = open('users.TXT', 'r').read().split(' ')
    for user in txt:
        try:
            bot.send_message(user, text='Привет всем')
        except:
            pass
    with open('logs.TXT', 'a') as logs:
        print(f'Пользователь {message.from_user.first_name} написал "{message.text}', file=logs)


@bot.message_handler(func= lambda message: message.text.lower() == 'рандомное фото')
def random_photo(message):
    url = "https://api.unsplash.com/photos/random?client_id=9xz-KB27jFOshFEus5HvgWEed2NohcyFu_E-wNOO3fM"
    response = requests.get(url)
    data = response.json()
    photo_url = data['urls']['regular']
    bot.send_photo(message.chat.id, photo=photo_url)
    with open('logs.TXT', 'a') as logs:
        print(f'Пользователь {message.from_user.first_name} написал "{message.text}', file=logs)


@bot.message_handler(func= lambda message: message.text.lower() == 'получить информацию обо мне')
def get_info(message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    nickname = message.from_user.username
    premium = message.from_user.is_premium
    file = open('users_full.TXT', 'r')
    txt = file.read()
    if str(message.chat.id) not in txt:
        file.close()
        file = open('users_full.TXT', 'a')
        file.write(f'ID - {message.chat.id}\nFirst name - {first_name}\nLast name - {last_name}\nNickname - {nickname}\nPremium - {premium} \n\n')
        file.close()
    if last_name is None:
        last_name = 'отсутсвует'
    if premium is None:
        premium = 'нет'
    else:
        premium = 'да'

    try:
        params = {'chat_id': str(message.chat.id)}
        response = requests.get(url=f'https://api.telegram.org/bot{token}/getChat', params=params)
        data = response.json()
        bio = data['result']['bio']
        print(bio)
    except:
        bio = 'Невозможно получить доступ к описанию профиля'
        print(bio)

    try:
        params = {'user_id': str(message.chat.id)}
        response = requests.get(url=f'https://api.telegram.org/bot{token}/getUserProfilePhotos', params=params)
        photo = response.json()
        photo = photo['result']['photos']
        photo = photo[0][-1]['file_id']
        bot.send_photo(message.chat.id, photo=photo, caption=f'Ваше имя: {first_name} '
                                                             f'\nВаша фамилия: {last_name} '
                                                             f'\nВаш псевдоним: {nickname} '
                                                             f'\nПремиум: {premium} '
                                                             f'\nОписание: {bio}')
    except:
        bot.send_message(message.chat.id, text=f'Ваше имя: {first_name} '
                                               f'\nВаша фамилия: {last_name} '
                                               f'\nВаш псевдоним: {nickname} '
                                               f'\nПремиум: {premium} '
                                               f'\nФото: невозможно получить фото '
                                               f'\nОписание: {bio}')

    with open('logs.TXT', 'a') as logs:
        print(f'Пользователь {message.from_user.first_name} написал "{message.text}'.encode('utf8'), file=logs, )


bot.polling()