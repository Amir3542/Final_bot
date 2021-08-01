from __future__ import unicode_literals
from time import sleep
from random import randint
from telegram import *
from const import *
import datetime as dt
import sqlite3
from sql_req import *
from time import sleep
import requests
from classes import *
from faker import Faker
import youtube_dl
import sys
import cv2
import requests
from bs4 import BeautifulSoup
import lxml
import COVID19Py


def start(update, context):
    user_id = update.message.chat_id
    name = update.message.from_user.first_name
    con = sqlite3.connect('Admin/db.sqlite')
    cur = con.cursor()
    id_in = cur.execute(select_id.format(user_id)).fetchall()
    try:
        id_in = id_in[0][0]
        context.bot.send_message(text='Добро пожаловать, я вас помню {}!'.format(name), chat_id=user_id)
        txt_answ(update, context)
    except IndexError:
        cur.execute(first_insert.format(user_id, name))
        con.commit()
        context.bot.send_message(text='Добро пожаловать, {}!'.format(name), chat_id=user_id)
        buttons = [InlineKeyboardButton(text='Русский', callback_data='rus'),
                   InlineKeyboardButton(text='English', callback_data='eng')]
        context.bot.send_message(text='Выберите язык', chat_id=user_id, reply_markup=InlineKeyboardMarkup([buttons]))


def rus(update, context):
    user_id = update.callback_query.from_user.id
    name = update.callback_query.from_user.first_name
    con = sqlite3.connect('Admin/db.sqlite')
    cur = con.cursor()
    cur.execute(update_lang.format('rus', user_id))
    cur.execute(select_lang.format('lang', user_id)).fetchall()
    context.bot.send_message(chat_id=user_id, text=MSG['rus'][0])
    btn = [KeyboardButton(text='Меню')]
    context.bot.send_message(chat_id=user_id, text=MSG['rus'][1],
                             reply_markup=ReplyKeyboardMarkup([btn], resize_keyboard=True))
    con.commit()


def eng(update, context):
    user_id = update.callback_query.from_user.id
    name = update.callback_query.from_user.first_name
    con = sqlite3.connect('Admin/db.sqlite')
    cur = con.cursor()
    cur.execute(update_lang.format('eng', user_id))
    x = cur.execute(select_lang.format('lang', user_id)).fetchall()
    context.bot.send_message(chat_id=user_id, text=MSG['eng'][0])
    btn = [KeyboardButton(text='Menu')]
    context.bot.send_message(chat_id=user_id, text=MSG['eng'][1],
                             reply_markup=ReplyKeyboardMarkup([btn], resize_keyboard=True))
    con.commit()


def helpa(update, context):
    user_id = update.message.chat_id
    name = update.message.from_user.first_name
    context.bot.send_message(chat_id=user_id,
                             text='Я бот для создания фейковых данных, получения адреса по локации, могу снять скриншот страницы сайта, скиньте URL и я верну вам фото')


def txt_answ(update, context):
    user_id = update.message.chat_id
    name = update.message.from_user.first_name
    text = update.message.text
    con = sqlite3.connect('Admin/db.sqlite')
    cur = con.cursor()
    x = cur.execute(select_stage.format('stage', user_id)).fetchall()
    y = cur.execute(select_lang.format('lang', user_id)).fetchall()
    con.commit()
    if text == 'Меню' or 'Menu':
        cur.execute(update_stage.format(1, user_id))
        con.commit()
        x = cur.execute(select_stage.format('stage', user_id)).fetchall()
        con.commit()
        btns = [KeyboardButton(text='Скриншот сайта'),
                KeyboardButton(text='Адрес по локации', request_location=True)]
        btns2 = [KeyboardButton(text='Генератор фейковых данных')]
        context.bot.send_message(chat_id=user_id, text='Выберите действие',
                                 reply_markup=ReplyKeyboardMarkup([btns, btns2], resize_keyboard=True))
        if text == 'В начало':
            start(update, context)
            cur.execute(update_stage.format(0, user_id))
            con.commit()
        # if text == 'Распознование лиц':
        #     context.bot.send_message(chat_id=user_id, text='Скиньте фото',
        #                              reply_markup=ReplyKeyboardMarkup([btns], resize_keyboard=True))
        #     sleep(20)
        #     photo_id = update.message.photo[-1].file_id
        #     file = context.bot.getFile(photo_id)
        #     file_name = 'Face.jpg'
        #     imgPath = file.download(file_name)
        #     faceCascade = cv2.CascadeClassifier(
        #         cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        #
        #     img = cv2.imread(imgPath)
        #     imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #
        #     faces = faceCascade.detectMultiScale(
        #         imgGray,
        #         scaleFactor=1.1,
        #         minNeighbors=4,
        #         minSize=(30, 30),
        #         flags=cv2.CASCADE_SCALE_IMAGE
        #     )
        #
        #     print(f"Найдено лиц: {len(faces)}")
        #
        #     if len(faces) != 0:
        #         print("Вывожу на экран ...")
        #
        #         for (x, y, w, h) in faces:
        #             cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 5)
        #
        #         cv2.imshow("Найденные лица", img)
        #         cv2.waitKey(0)

        # if text == 'Скачать ютуб видео':
        #     btn = [KeyboardButton(text='1 видео'),
        #            KeyboardButton(text='2 видео'),
        #            KeyboardButton(text='3 видео')]
        #     context.bot.send_message(chat_id=user_id, text='Выберите видео',
        #                              reply_markup=ReplyKeyboardMarkup([btn], resize_keyboard=True))
        # if text == '1 видео':
        #     def progress_hook(d):
        #         if d['status'] == "downloading":
        #             print(f'{d["_speed_str"]} ({d["_percent_str"]})')
        #         else:
        #             print("Готово!")
        #
        #     ydl_opts = {
        #         'progress_hooks': [progress_hook]
        #     }
        #
        #     link = 'https://www.youtube.com/watch?v=DhzeU7l4sWo'
        #
        #     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        #         ydl.download([link])
        #
        #     pat = 'video.mp3'
        #     with open(pat, 'wb') as file:
        #         for i in ydl:
        #             file.write(i)
        #     context.bot.send_video(chat_id=user_id, video=open(pat, 'rb'), caption='Вот оно')

        if text == 'Генератор фейковых данных':
            cur.execute(update_stage.format(2, user_id))
            con.commit()
            fake = Faker()

            a = f'{fake.name()}, {fake.address()}, {fake.country()}, {fake.city()}, {fake.job()}'
            context.bot.send_message(chat_id=user_id,
                                     text=str(a).format('Имя: {}', 'Адрес: {}', 'Страна: {}', 'Город: {}',
                                                        'Работа: {}'),
                                     reply_markup=ReplyKeyboardMarkup([btns, btns2], resize_keyboard=True))
            if user_id != ADMIN_ID:
                context.bot.send_message(
                    text='Пользователь: {},\nс id: {} нажал на кнопку:\nГенератор фейковых данных'.format(name, user_id),
                    chat_id=ADMIN_ID)
        if text == 'Скриншот сайта':
            cur.execute(update_stage.format(3, user_id))
            con.commit()
            context.bot.send_message(chat_id=user_id, text='Жду ссылку',
                                     reply_markup=ReplyKeyboardMarkup([btns, btns2], resize_keyboard=True))
            if user_id != ADMIN_ID:
                context.bot.send_message(
                    text='Пользователь: {},\nс id: {} нажал на кнопку:\nСкриншот сайта'.format(name, user_id),
                    chat_id=ADMIN_ID)
    if text[:4] == 'http':
        counter = 0
        BASE = 'https://render-tron.appspot.com/screenshot/'
        url = text
        path = 'screen.jpg'
        response = requests.get(BASE + url, stream=True)
        # save file, see https://stackoverflow.com/a/13137873/7665691
        if response.status_code == 200:
            with open(path, 'wb') as file:
                for chunk in response:
                    file.write(chunk)

        context.bot.send_photo(chat_id=user_id, photo=open(path, 'rb'), caption='Вот скриншот')
        if user_id != ADMIN_ID:
            context.bot.send_photo(
                caption='Пользователь: {},\nс id: {} Снял скриншот этого сайта'.format(name, user_id),
                chat_id=ADMIN_ID, photo=open(path, 'rb'))


def get_address_from_coords(coords):
    PARAMS = {
        "apikey": "404a4ae0-ef18-4719-9e54-f79aa01b4a9f",
        "format": "json",
        "lang": "ru_RU",
        "kind": "house",
        "geocode": coords
    }

    try:
        r = requests.get(url="https://geocode-maps.yandex.ru/1.x/", params=PARAMS)
        json_data = r.json()
        address_str = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"][
            "GeocoderMetaData"]["AddressDetails"]["Country"]["AddressLine"]
        return address_str

    except Exception as e:
        return "Не могу определить адрес по этой локации"


def location(update, context):
    message = update.message
    current_position = (message.location.longitude, message.location.latitude)
    coords = f"{current_position[0]},{current_position[1]}"
    address_str = get_address_from_coords(coords)
    update.message.reply_text(address_str)
