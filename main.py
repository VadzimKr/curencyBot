import telebot
import requests
from telebot import types
import time

with open("TOKEN.ini") as t_file:
    TOKEN = t_file.read()
bot = telebot.TeleBot(TOKEN)
with open("API.ini") as api_file:
    OPENEXCHANGE_API_KEY = api_file.read()
bot = telebot.TeleBot(TOKEN)


png_urls = {'USD': 'https://telegra.ph/file/1257426aee59fc94d6290.png',
            'EUR': 'https://telegra.ph/file/003a59d8017afc3aba571.png',
            'PLN': 'https://telegra.ph/file/e615ad921d48910222eca.png',
            'BYN': 'https://telegra.ph/file/15d4b8ecee8929bc51927.png',
            'RUB': 'https://telegra.ph/file/25747932f93b6db5cd3a0.png'}
png = ['https://telegra.ph/file/be3af86e7933d344769f7.png',
       'https://telegra.ph/file/0efc66e24910406494aef.png',
       'https://telegra.ph/file/73cd236ca7d888d8ac75d.png',
       'https://telegra.ph/file/db4523946134d43838254.png',
       'https://telegra.ph/file/dd351b18fdd10e971834b.png',
       'https://telegra.ph/file/0dc6d208d72d851aa31f7.png']
curencies = ['USD', 'PLN', 'EUR', 'BYN', 'RUB']
error_png ='https://telegra.ph/file/78ce78feeb816cf870c2c.png'

@bot.inline_handler(func=lambda query: len(query.query) == 0)
def empty_query(query):
    hint = "Введите идентификаторы валют: USD, PLN, EUR, BYN, RUB чтобы узнать курс валюты"
    try:
        r = types.InlineQueryResultArticle(
                id='1',
                title="Бот \"Валютчик\"",
                description=hint,
                input_message_content=types.InputTextMessageContent(
                message_text="А мог бы узнать курс валют...",
                parse_mode='Markdown')
        )
        bot.answer_inline_query(query.id, [r])
    except Exception as e:
        print(e)
        error_fun("Ошибка", e, query)


def curency2(cur1, cur2, query):
    rate = kostil(cur1, cur2)
    # Генерация текста полученного ответа
    result1 = f"1 {cur1} = {round(rate, 4)} {cur2}"
    result2 = f"5 {cur1} = {round(rate * 5, 2)} {cur2}"
    result3 = f"10 {cur1} = {round(rate * 10, 2)} {cur2}"
    result4 = f"20 {cur1} = {round(rate * 20, 2)} {cur2}"
    result5 = f"50 {cur1} = {round(rate * 50, 2)} {cur2}"
    result6 = f"100 {cur1} = {round(rate * 100, 2)} {cur2}"

    # Generate an InlineQueryResultArticle object with the currency conversion result
    article1 = telebot.types.InlineQueryResultArticle(
        id='1', title='1', description=result1,
        input_message_content=telebot.types.InputTextMessageContent(message_text=result1),
        thumbnail_url=png[0], thumbnail_width=64, thumbnail_height=64)
    article2 = telebot.types.InlineQueryResultArticle(
        id='2', title='5', description=result2,
        input_message_content=telebot.types.InputTextMessageContent(message_text=result2),
        thumbnail_url=png[1], thumbnail_width=64, thumbnail_height=64)
    article3 = telebot.types.InlineQueryResultArticle(
        id='3', title='10', description=result3,
        input_message_content=telebot.types.InputTextMessageContent(message_text=result3),
        thumbnail_url=png[2], thumbnail_width=64, thumbnail_height=64)
    article4 = telebot.types.InlineQueryResultArticle(
        id='4', title='20', description=result4,
        input_message_content=telebot.types.InputTextMessageContent(message_text=result4),
        thumbnail_url=png[3], thumbnail_width=64, thumbnail_height=64)
    article5 = telebot.types.InlineQueryResultArticle(
        id='5', title='50', description=result5,
        input_message_content=telebot.types.InputTextMessageContent(message_text=result5),
        thumbnail_url=png[4], thumbnail_width=64, thumbnail_height=64)
    article6 = telebot.types.InlineQueryResultArticle(
        id='6', title='100', description=result6,
        input_message_content=telebot.types.InputTextMessageContent(message_text=result6),
        thumbnail_url=png[5], thumbnail_width=64, thumbnail_height=64)
    # Отправляем ответ пользователю
    bot.answer_inline_query(query.id, [article1, article2, article3, article4, article5, article6])


def kostil(cur1, cur2):
    # Определяем адрес запроса для API.
    url2 = f"https://openexchangerates.org/api/latest.json?app_id={OPENEXCHANGE_API_KEY}&base=USD&symbols={cur2}"
    # Отправка GET запроса к API
    response = requests.get(url2)
    # Парсинг (расшифровка) полученного ответа
    rate2 = response.json()['rates'][cur2]
    if cur1 == 'USD':
        return rate2
    else:
        url1 = f"https://openexchangerates.org/api/latest.json?app_id={OPENEXCHANGE_API_KEY}&base=USD&symbols={cur1}"
        response = requests.get(url1)
        rate1 = response.json()['rates'][cur1]
        rate = rate2 / rate1
        return rate


# Генерация текста полученного ответа
def curency1(cur1, query):
    results = []
    articles = []
    i = 0
    for cur2 in curencies:
        if cur1 != cur2:
            rate = kostil(cur1, cur2)
            # Генерация текста полученного ответа
            result = f"1 {cur1} = {round(rate, 4)} {cur2}"
            results.append(result)
            #  Генерация InlineQueryResultArticle объектов, которые потом будут отправлены пользователю
            article = telebot.types.InlineQueryResultArticle(
                id=i, title=cur2, description=results[i],
                input_message_content=telebot.types.InputTextMessageContent(message_text=results[i]),
                thumbnail_url=png_urls[cur2], thumbnail_width=64, thumbnail_height=64)
            articles.append(article)
            i += 1
    # Отправляем ответ пользователю
    bot.answer_inline_query(query.id, articles)

def curency3(cur1, cur2, q, query):
    rate = kostil(cur1, cur2)
    # Генерация текста полученного ответа
    result = f"{q} {cur1} = {round(rate * float(q))} {cur2}"
    #  Генерация InlineQueryResultArticle объектов, которые потом будут отправлены пользователю
    article = telebot.types.InlineQueryResultArticle(
        id=1, title=cur2, description=result,
        input_message_content=telebot.types.InputTextMessageContent(message_text=result),
        thumbnail_url=png_urls[cur2], thumbnail_width=64, thumbnail_height=64)
    # Отправляем ответ пользователю
    bot.answer_inline_query(query.id, [article])


def curency1_plus_num(cur1, q, query):
    results = []
    articles = []
    i = 0
    for cur2 in curencies:
        if cur1 != cur2:
            rate = kostil(cur1, cur2)
            # Генерация текста полученного ответа
            result = f"{q} {cur1} = {round(rate*q, 2)} {cur2}"
            results.append(result)
            #  Генерация InlineQueryResultArticle объектов, которые потом будут отправлены пользователю
            article = telebot.types.InlineQueryResultArticle(
                id=i, title=cur2, description=results[i],
                input_message_content=telebot.types.InputTextMessageContent(message_text=results[i]),
                thumbnail_url=png_urls[cur2], thumbnail_width=64, thumbnail_height=64)
            articles.append(article)
            i += 1
    # Отправляем ответ пользователю
    bot.answer_inline_query(query.id, articles)

@bot.inline_handler(lambda query: query.query)
def query_text(query):
    # Разделяем полученную в запросе информацию
    req = query.query.upper().split()
    if len(req) == 2:
        src, tgt = req
        if req[1] in curencies and req[0] in curencies:
            curency2(src, tgt, query)
        elif req[0] not in curencies:
            if is_numer(req[0]) and req[1] in curencies:
                curency1_plus_num(req[1], float(req[0]), query)
            else:
                # Генерация текста полученного ответа
                result = f"Простите, но запрос {req[0]} не был распознан. Введите валюту или число."
                error_fun('Ошибка ввода', result, query)
        elif req[1] not in curencies:
            if is_numer(req[1]) and req[0] in curencies:
                curency1_plus_num(req[0], float(req[1]), query)
            else:
                # Генерация текста полученного ответа
                result = f"Простите, но запрос {req[1]} не был распознан. Введите валюту или число."
                error_fun('Ошибка ввода', result, query)
    elif len(req) == 1:
        if req[0] in curencies:
            curency1(req[0], query)
        else:
            # Генерация текста полученного ответа
            result = f"Простите, но запрос {req[0]} не был распознан в качестве валюты."
            error_fun('Ошибка ввода валюты', result, query)
    elif len(req) == 3:
        src, tgt, quantity = req
        if req[0] in curencies and req[1] in curencies and is_numer(req[2]):
            curency3(src, tgt, quantity, query)
        elif req[0] not in curencies:
            # Генерация текста полученного ответа
            result = f"Простите, но запрос {req[0]} не был распознан в качестве валюты."
            error_fun('Ошибка ввода валюты', result, query)
        elif req[1] not in curencies:
            # Генерация текста полученного ответа
            result = f"Простите, но запрос {req[1]} не был распознан в качестве валюты."
            error_fun('Ошибка ввода валюты', result, query)
        elif not is_numer(req[2]):
            result = f"Простите, но запрос {req[2]} не был распознан в качестве положительного числа"
            error_fun('Ошибка ввода количества единиц валюты', result, query)
    elif len(req) > 3:
        result = f"Я умею обрабатывать только запросы от 1 до 3 параметров. Пожалуйста, перепишите запрос."
        error_fun('Ошибка количества параметров', result, query)
    else:
        result = f"Я не знаю, с чем связана эта ошибка. \n" \
                 f"Не могли бы вы отправить скриншот запроса моему создателю?\n" \
                 f"Его аккаунт @itstudenteu"
        error_fun('Неизвестная ошибка', result, query)



def error_fun(title, text, query):
     #  Генерация InlineQueryResultArticle объектов, которые потом будут отправлены пользователю
    article = telebot.types.InlineQueryResultArticle(
        id=1, title=title, description=text,
        input_message_content=telebot.types.InputTextMessageContent(message_text=text),
        thumbnail_url=error_png, thumbnail_width=64, thumbnail_height=64)
    # Отправляем ответ пользователю
    bot.answer_inline_query(query.id, [article])


def is_numer(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
# Команда start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, """Привет!🤗 Я твой инлайн бот для подсчёта курсов валют. Ты можешь написать мне из \
любого открытого чата и я помогу тебе перевести деньги из одной валюты в другую. В своей \
работе я использую курсы валют с сайта https://openexchangerates.org/\n
Если захочешь узнать обо мне побольше, просто используй команду \n/help""")


@bot.message_handler(commands=["help"])
def start(m, res=False):
    bot.send_message(m.chat.id, """Привет!🤗 Я твой инлайн бот для подсчёта курсов валют. Ты можешь написать мне из \
любого открытого чата и я помогу тебе перевести деньги из одной валюты в другую. В своей работе я использую курсы валют\
 с сайта openexchangerates.org/\n\n""")
    time.sleep(2)
    bot.send_message(m.chat.id, """
Давай представим, что я хочу написать своей бабушке🧑‍🦳, как дёшево я могу купить машину в стране своего проживания. Но \
бабушка живёт в другой стране с другой валютой. Что же делать?\n\nВсё очень просто! \n👆 Первый шаг: открой чат с \
бабушкой и вызови меня. Сделать это можно просто нажав символ "собака" и вписав  моё имя. Вот так: \n 
@curency_change_bot\n\n ✌️ Второй шаг: Напиши запрос. Какими могут быть запросы? \n\n""")
    time.sleep(8)
    bot.send_message(m.chat.id, """
-1️⃣ пример запроса. Я могу написать сумму и валюту, в которой номинирована эта сумма:\n
@curency_change_bot 120500 PLN \n
Этот запрос заставит меня найти стоимость польского злотого к остальным валютам моего списка, а затем  умножить эту \
стоимость на сумму и округлить результат до копеек.\n\n""")
    time.sleep(8)
    bot.send_message(m.chat.id, """
-2️⃣ пример запроса. Я хочу узнать стоимость одной единицы моей валюты к другим. \
Я просто ввожу:\n @curency_change_bot BYN\n И получаю стоимость к основным валютам \
моего списка, округлённую до четвёртого знака.\n\n""")
    time.sleep(8)
    bot.send_message(m.chat.id, """
-3️⃣ пример. Я хочу перевести сумму из одной валюты в другую и для этого пишу:\n
@curency_change_bot BYN PLN 1204.5\n
Этот запрос позволит мне узнать, сколько в злотых будет 1204.5 белорусских рублей.\n
❗️ВНИМАНИЕ: если сумма включает копейки(центы), то они должны отделяться точкой\n
❗️❗️ВНИМАНИЕ2: Сперва пишите в какой валюте номинирована сумма, а уже затем, в какой валюте будет результат. \n\n
Я надеюсь, я буду тебе полезен. Если у тебя возникнут вопросы по моей работе - обращайся к моему создателю, \
Вадиму Крючкову @itstudenteu\n\n""")
    time.sleep(20)
    bot.send_message(m.chat.id, """А если хочешь создать своего бота-записывайся на бесплатное пробное занятие \
по Python. \n https://calendly.com/itstudent/50min-tg""")

bot.polling()