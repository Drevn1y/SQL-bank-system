import sqlite3

def login():
    login_name = input('Введите имя: ')
    login_last_name = input('Введите фамилию: ')
    login_sure_name = input('Введите отчество: ')
    login_phone_number = input('Введите номер телефона: ')

    search = sql.execute("""SELECT balance FROM bank 
                                       WHERE first_name=? AND last_name=? AND surname=? AND phone_number=?;""",
                         (login_name, login_last_name, login_sure_name, login_phone_number))
    result = search.fetchone()
    print('Ваш балланс: ', result)

def plus():
    login_name = input('Введите имя: ')
    login_last_name = input('Введите фамилию: ')
    login_sure_name = input('Введите отчество: ')
    login_phone_number = input('Введите номер телефона: ')

    search = sql.execute("""
        SELECT balance FROM bank 
        WHERE first_name=? AND last_name=? AND surname=? AND phone_number=?;
    """, (login_name, login_last_name, login_sure_name, login_phone_number))

    result = search.fetchone()

    if result:
        current_balance = result[0]  # Извлекаем баланс из кортежа
        print('Ваш баланс: ', current_balance)

        balance_plus = float(input('Введите сумму пополнения: '))
        new_balance = current_balance + balance_plus
        print('Новый баланс: ', new_balance)

        # Обновляем баланс в базе данных
        sql.execute("""
            UPDATE bank SET balance=? 
            WHERE first_name=? AND last_name=? AND surname=? AND phone_number=?;
        """, (new_balance, login_name, login_last_name, login_sure_name, login_phone_number))

    else:
        print('Пользователь не найден.')

def minus():
    login_name = input('Введите имя: ')
    login_last_name = input('Введите фамилию: ')
    login_sure_name = input('Введите отчество: ')
    login_phone_number = input('Введите номер телефона: ')

    search = sql.execute("""
            SELECT balance FROM bank 
            WHERE first_name=? AND last_name=? AND surname=? AND phone_number=?;
        """, (login_name, login_last_name, login_sure_name, login_phone_number))

    result = search.fetchone()

    if result:
        current_balance = result[0]  # Извлекаем баланс из кортежа
        print('Ваш баланс: ', current_balance)

        balance_minus = float(input('Введите сумму вывода: '))
        if current_balance <= balance_minus:
            new_balance = current_balance - balance_minus
            print('Новый баланс: ', new_balance)
            # Обновляем баланс в базе данных
            sql.execute("""
                    UPDATE bank SET balance=? 
                    WHERE first_name=? AND last_name=? AND surname=? AND phone_number=?;
                """, (new_balance, login_name, login_last_name, login_sure_name, login_phone_number))
        else:
            print('Недостаточно средств!')
    else:
        print('Пользователь не найден.')

# Подключение к базе данных
connection = sqlite3.connect('Bank.db')
# Python + SQL
sql = connection.cursor()

# Создание таблицы
sql.execute("""CREATE TABLE IF NOT EXISTS bank(
first_name TEXT,
last_name TEXT,
surname TEXT,
phone_number TEXT,
balance REAL);""")

# # Добавление данных в таблицу
# sql.execute("""INSERT INTO bank (
#     first_name,
#     last_name,
#     surname,
#     phone_number,
#     balance
# ) VALUES (
#     'Илон',
#     'Маск',
#     'Теслов',
#     '+998(99)123-45-67',
#     7000
# );""")
while True:
    manager = input("Что вы хотите сделать? ")
    if manager.title() == 'Регистрация':
        # Новый клиент
        f_name = input('Введите имя: ')
        l_name = input('Введите фамилию: ')
        s_name = input('Введите отчество: ')
        p_number = input('Введите номер телефона: ')
        n_balance = input('Введите балланс: ')

        sql.execute("""INSERT INTO bank (
            first_name, 
            last_name, 
            surname, 
            phone_number, 
            balance 
        ) VALUES (?, ?, ?, ?, ?);""",(f_name, l_name, s_name, p_number, n_balance))
    elif manager.title() == 'База Данных':
    #Поиск в баззе данных
        system01 = input('1. Посмотреть всех\n2. Поиск\n')
        if system01 == '1':
            print(sql.execute('SELECT * FROM bank').fetchall())
        elif system01 == '2':
            sf_name = input('Введите имя: ')
            sl_name = input('Введите фамилию: ')
            ss_name = input('Введите отчество: ')
            sp_number = input('Введите номер телефона: ')

            search = sql.execute("""SELECT * FROM bank 
                                   WHERE first_name=? AND last_name=? AND surname=? AND phone_number=?;""",
                                 (sf_name, sl_name, ss_name, sp_number))
            result = search.fetchall()
            print(result)
        else:
            print('Выберите от 1 до 2!')

    elif manager.title() == 'Личный Кабинет':
        print('1. Пополнение баланса\n2. снятие денег с баланса\n3. Просмотр баланса\n4. Подсчет вклада ')
        user = int(input('Что вы хотите сделать? '))
        if user == 1:
            plus()
        elif user == 2:
            minus()
        elif user == 3:
            login()
        elif user == 4:
            print('=====Подсчет вклада=====')
            vklad = float(input('Введите сумму вклада: '))
            #логика
            print('===Подсказка===\nЕсли хотите увидеть все результаты введите 0')
            percent = int(input('Введите процентную ставку(12 24 36): '))
            if percent == 12:
                p1 = ((1 + (0.12)/10) ** 10 * 1) * vklad - vklad
                print(p1)
            elif percent == 24:
                p2 = ((1 + (0.12)/10) ** 10 * 2) * 100 - 100
                print(p2)
            elif percent == 36:
                p3 = ((1 + (0.12) / 10) ** 10 * 3) * 100 - 100
                print(p3)
            elif percent == 0:
                p1 = ((1 + (0.12)/10) ** 10 * 1) * vklad - vklad
                p2 = ((1 + (0.12) / 10) ** 10 * 2) * vklad - vklad
                p3 = ((1 + (0.13) / 10) ** 10 * 3) * vklad - vklad
                print('14: ', p1)
                print('24: ', p2)
                print('36: ', p3)
            else:
                print('Введите только 12 ил 24 или 36 или 0')


    elif manager == '/help':
        print('Список команд📖\n1. Регистрация\n2. База данных\n3. Личный кабинет\n4. Выход')
    elif manager.title() == 'Выход':
        # Закрепляем изменения
        connection.commit()
        break
    else:
        print('Увы, такой команды нет!\nЕсли вам нужна помошь, напишите команду /help')

    # Закрепляем изменения
    connection.commit()
