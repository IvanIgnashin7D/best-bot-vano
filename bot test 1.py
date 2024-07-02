from telebot import *
from types import *
import requests
import logging
from dotenv import load_dotenv
import os
from googletrans import Translator
from time import sleep


load_dotenv()
UNSPLASH_API_KEY = os.getenv('CLIENT_ID')
token = os.getenv('TOKEN')
bot = TeleBot(token=token)
logging.basicConfig(filename='logs.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
translator = Translator()
photo_info = {}

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=False)
button1 = types.KeyboardButton(text='Написать сообщение с ссылками')
button2 = types.KeyboardButton(text='Отправить фото с подписью')
button3 = types.KeyboardButton(text='Отправить одну ссылку')
button4 = types.KeyboardButton(text='Отправить всем привет')
button5 = types.KeyboardButton(text='Рандомное фото')
button6 = types.KeyboardButton(text='Получить информацию обо мне')
keyboard.add(button1, button2, button3, button4, button5, button6)



@bot.message_handler(commands=['start'])
def privet(message):
    global keyboard
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


@bot.message_handler(commands=['ssilki'])
@bot.message_handler(func= lambda message: message.text == 'Написать сообщение с ссылками')
def send_ssilki(message):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text='Vikipedia', url='https://ru.wikipedia.org/wiki/%D0%92%D0%B8%D0%BA%D0%B8%D0%BF%D0%B5%D0%B4%D0%B8%D1%8F')
    button2 = types.InlineKeyboardButton(text='Telegram', url='https://ru.wikipedia.org/wiki/Telegram')
    keyboard.add(button1, button2)
    bot.send_message(message.chat.id, text='Вот кнопки с ссылками:', reply_markup=keyboard)
    logging.info(f'Пользователь {message.from_user.first_name} написал: {message.text}. Бот отправил кнопки с ссылками.')


@bot.message_handler(commands=['photo'])
@bot.message_handler(func= lambda message: message.text == 'Отправить фото с подписью')
def send_photo(message):
    photo = open('x_915201e5.jpg', 'rb')
    bot.send_photo(message.chat.id, photo, caption='Вот фото сверху')
    logging.info(f'Пользователь {message.from_user.first_name} написал: {message.text}. Бот отправил фото с подписью.')


@bot.message_handler(commands=['ssilka'])
@bot.message_handler(func= lambda message: message.text == 'Отправить одну ссылку')
def send_ssilka(message):
    bot.send_message(message.chat.id, text='Вот ссылка на гугл: https://www.google.ru/')
    logging.info(f'Пользователь {message.from_user.first_name} написал: {message.text}. Бот отправил ссылку на гугл.')


@bot.message_handler(func=lambda message: message.text.lower() == 'отправить всем привет')
def hello_all(message):
    txt = open('users.TXT', 'r').read().split(' ')
    for user in txt:
        try:
            bot.send_message(user, text='Привет всем')
            logging.info(f'Пользователь {message.from_user.first_name} написал: {message.text}. Бот всем написал привет.')
        except:
            logging.error(f'Пользователь {message.from_user.first_name} написал: {message.text}. ОШИБКА при отправке ответа.')


@bot.message_handler(func=lambda message: message.text.lower() == 'рандомное фото')
def random_photo_ask_query(message):
    sent = bot.send_message(message.chat.id, text='Напишите тему фотографии ОДНИМ словом')
    bot.register_next_step_handler(sent, random_photo_ask_count)

def random_photo_ask_count(message):
    photo_info['query'] = message.text
    sent = bot.send_message(message.chat.id, text='Напишите цифрой сколько изображений вы хотите? (не более 10)')
    bot.register_next_step_handler(sent, random_photo_answer)

def random_photo_answer(message):
    global keyboard
    translated_text = translator.translate(photo_info['query']).text
    url = f"https://api.unsplash.com/photos/random?client_id={UNSPLASH_API_KEY}"
    params = {'count': message.text, 'query': translated_text}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        photos = [types.InputMediaPhoto(media=data[i]['urls']['regular']) for i in range(int(message.text))]
        bot.send_media_group(message.chat.id, media=photos)
        bot.send_message(message.chat.id, text='Выберите действие:', reply_markup=keyboard)
        logging.info(f'Пользователь {message.from_user.first_name} написал: {message.text}. Бот отправил 3 фото.')
    else:
        bot.send_message(message.chat.id, text='Произошла ошибка при отправке фото( '
                                               '\nВведите другую тему или повторите попытку позже.', reply_markup=keyboard)
        logging.error(f'ОШИБКА при отправке фото. КОД ОТВЕТА {response.status_code}')


@bot.message_handler(func= lambda message: message.text.lower() == 'получить информацию обо мне')
def get_info(message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    nickname = message.from_user.username
    premium = message.from_user.is_premium
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
    except:
        bio = 'Невозможно получить доступ к описанию профиля'

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
        logging.info(f'Пользователь {message.from_user.first_name} написал: {message.text}. Бот отправил инфо и фото пользователя.')
    except:
        bot.send_message(message.chat.id, text=f'Ваше имя: {first_name} '
                                               f'\nВаша фамилия: {last_name} '
                                               f'\nВаш псевдоним: {nickname} '
                                               f'\nПремиум: {premium} '
                                               f'\nФото: невозможно получить фото '
                                               f'\nОписание: {bio}')
        logging.info(f'Пользователь {message.from_user.first_name} написал: {message.text}. Бот отправил инфо пользователя без фото.')


while True:
    try:
        bot.polling()
    except:
        logging.critical("КРИТИЧЕСКАЯ ОШИБКА В РАБОТЕ БОТА")
        sleep(60)
        continue