import sqlite3

# Подключаемся к базе данных
conn = sqlite3.connect("telegram_bot.db", check_same_thread=False)
cursor = conn.cursor()


# Функция проверки есть ли ид пользователь в базе данных, т.е. первое ли его использование данного бота
def users(user_id):
    cursor.execute('''SELECT user_id FROM user WHERE user_id =?''', (user_id,))
    conn.commit()
    use = cursor.fetchall()
    # если fetchall позвращает пустое значение т.е. [], значит данного пользователя нету в базе данных
    if use != []:
        return True
    else:
        return False


# Функция ид пользователя в базу данных
def add_user(user_id):
    cursor.execute('''INSERT INTO user(user_id) VALUES(?)''', (user_id,))
    conn.commit()


# Функция для вывода списка вопросов из базы данных
def info_ask():
    cursor.execute('''SELECT ask FROM ask''')
    conn.commit()
    info = cursor.fetchall()
    str_1 = ''
    for i in info:
        for x in i:
            str_1 += str(x) + '\n'
    return str_1


# Функция возвращения списка вопросов, для проверки есть ли вопрос заданный пользователем в боте в базе данных
def ask():
    cursor.execute('''SELECT ask FROM ask''')
    conn.commit()
    info = cursor.fetchall()
    asks = list()
    for i in info:
        for x in i:
            asks.append(str(x).lower()) # переводим все к нижнему регистру для удобства
    return asks


# Функция принимает значение заданного вопроса в боте, ищет его в базе данных и возвращает значение ответа для этого вопроса
def ask_answer(asks):
    cursor.execute('''SELECT ask, answer FROM ask WHERE ask = ?''', (asks.capitalize(),))
    conn.commit()
    info = cursor.fetchall()
    if asks.capitalize() == info[0][0]:
        return str(info[0][1])


