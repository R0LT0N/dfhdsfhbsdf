# -*- coding: utf8 -*-
import config
import telebot
import sqlite3
import string
import random
from telebot import types
import datetime
from datetime import *
import os
import time as t
import requests

buttons_start = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

bot = telebot.TeleBot(config.token)
print('Бот включен! '+str(datetime.now()))

db = sqlite3.connect('database.db', check_same_thread=False)
sql = db.cursor()
print('База данных подключена! '+str(datetime.now()))

sql.execute("""CREATE TABLE IF NOT EXISTS users (
	id INT PRIMARY KEY,
	login TEXT,
	fname TEXT,
	alllogs INT,
	datereg TEXT,
	status INT
)""")

sql.execute("""CREATE TABLE IF NOT EXISTS infoteam (
	numbers INT PRIMARY KEY,
	alllogsteam INT,
	dateopenteam TEXT
)""")

sql.execute(f"SELECT numbers FROM infoteam")
if sql.fetchone() is None:
	dt_now = str(datetime.today().strftime('%d.%m.%Y'))
	sql.execute(f"INSERT OR IGNORE INTO infoteam VALUES (?, ?, ?)", (1, 1, dt_now))
	db.commit()

@bot.message_handler(commands=['start'])
def send_welcome(message):
		sql = db.cursor()
		sql.execute(f"SELECT id FROM users WHERE id = '{message.chat.id}'")
		if sql.fetchone() is None:
			dt_now = str(datetime.today().strftime('%d.%m.%Y'))
			sql.execute(f"INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?, ?)", (message.chat.id, message.from_user.username, message.from_user.first_name, 1, dt_now, 1))
			db.commit()
		bot.send_message(message.chat.id,'База данных создана! Закройте окно этого кода!', parse_mode='HTML', reply_markup=buttons_start)
bot.polling(none_stop=True)
