import re
import os
from datetime import datetime


alphabet = 'abcdefghijklmnopqrstuvwxyz'
len_alpha = len(alphabet)


def encryption(Text, m_key, a_key):    # Зашифрование текста
    result = ''
    for word in Text:
        r_word = ord(word) - 65
        c = ((r_word * m_key) + a_key) % len(alphabet)
        res = chr(c + 65)
        result += res
    return result


access_list = ['r/w/e', 'r/w', 'r']


def create_user(username, password):
    with open("time.txt", 'a') as f:
        f.write(f'{username} {0}\n')
        f.close()
    with open("db.txt", 'a') as file:
        dec_pwd = encryption(password, 5, 6)
        file.write(f'{username} {dec_pwd}\n')
        file.close()
    with open('log.txt', 'a') as log:
        log.write(f'Created user - {username} at {datetime.now()}\n')
        log.close()


def login(username, password):
    with open("db.txt", "r") as file:
        if f'{username} {encryption(password, 5, 6)}\n' in file:
            return True
        else:
            print('Incorrect password or username. Please try again!')
            return False

def create_file(username):
    mas = []
    with open("db.txt", 'a') as file:
        file = input("Введите название файла: ")
        my_file = open(f'files/{file}', "w+")
        my_file.close()
        access = 'o/r/w/e'
        mas.extend([file, access])

    with open('access.txt', 'a') as access:
        access.write(f'{username} {mas}\n')

    return file


def grant_access(sub_user, access_list, file_name):
    with open ('access.txt', 'a') as file:
        choice = int(input('1 - "r/w/e", 2 - "r/w", 3 - "r": ')) - 1
        file.write(f'{sub_user} {[file_name, access_list[choice]]}\n')
        file.close()
    return access_list[choice]


def time(username):
    with open('time.txt', 'r+') as new_file:
        old_lines = new_file.readlines()  # Reads the lines from the files as a list
        new_file.seek(0)  # Seeks back to index 0
        for line in old_lines:
            line = line.split(' ')
            if line[0] == username:
                line[-1] = str(f'{int(line[-1]) + 1}\n')  # replace the text
            line = ' '.join(line)
            new_file.write(line)  # write to file


def del_user(username):
    f = open('db.txt').read()
    f = f.replace(f'{username}', '')


choice = int(input('1 - Registration, 2-login, 3-delete user:    '))

if choice == 1:
    username = input('username: ')
    password = input('password: ')
    while True:
        res = password.find('?')
        res2 = password.find('%')
        if res != -1 or res2 != -1:
            print('Пароль не дожен содержать символы (?, %)')
            password = input('password: ')
        elif len(password) < 5:
            print('Длина пароля должен быть не менее 5!')
            password = input('password: ')
        else:
            create_user(username, password)
            break


if choice == 2:
    a = []
    username = input('username: ')
    password = input('password: ')
    if login(username, password):
        with open('log.txt', 'a') as log:
            log.write(f'Выполнен вход в систему: пользователь - {username}\n')
            log.close()
        a.append(username)
        v = int(input('1 - dir\n2 - удалить файл\n3 - предоставить доступ\n4 - создать файл\n5 - выход\nВаш выбор: '))
        if v == 1:
            with open('access.txt', 'r+') as file:
                a = file.readlines()
                for i in a:
                    if f'{username} ' in i:
                        print(i)
        elif v == 2:
            with open('access.txt', 'r+') as file:
                w = input('Введите название файла: ')
                a = file.readlines()
                t = False
                for i in a:
                    if f"{username} ['{w}', 'o/r/w/e']\n" in i:
                        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), f'files/{w}')
                        os.remove(path)
                        t = True
                        i = i.replace(i, '')
                if t:
                    file.seek(0)
                    for j in a:
                        if j != f"{username} ['{w}', 'o/r/w/e']\n":
                            file.write(j)
                    file.truncate()
                    file.seek(0)
                    for j in a:
                        if w not in j:
                            file.write(j)
                    file.truncate()
                    file.close()
                else:
                    print("У вас нет права на удаление")
        elif v == 3:
            r = False
            with open('access.txt', 'r+') as file:
                w = input('Введите название файла: ')
                a = file.readlines()
                t = False
                for i in a:
                    if f"{username} ['{w}', 'o/r/w/e']\n" in i:
                        r = True
            c = False
            if r:
                user = input("Введите username: ")
                with open('db.txt', 'r+') as f:
                    for i in f:
                        if user in i:
                            q = grant_access(user, access_list, w)
                            print(q)
                            c = True
                            with open('log.txt', 'a') as log:
                                log.write(f'Субьект - {username} дал доступ к субьекту {user} на право [{q}]\n')
                                log.close()

                    if not c:
                        print('Такого пользователя нет')
        elif v == 4:
            res = create_file(username)
            time(username)
            ch = input('Хотите предоставить доступ пользователям? (y/n): ')
            if ch == 'y':
                c = False
                user = input("Введите username: ")
                with open('db.txt', 'r+') as f:
                    for i in f:
                        if user in i:
                            q = grant_access(user, access_list, res)
                            print(q)
                            c = True
                            with open('log.txt', 'a') as log:
                                log.write(f'Субьект - {username} дал доступ к субьекту {user} на право [{q}]\n')
                                log.close()

                    if not c:
                        print('Такого пользователя нет')
            print(res)
        elif v == 5:
            quit()


elif choice == 3:
    user = input("Enter the username: ")
    pattern = re.compile(re.escape(user))
    with open('db.txt', 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        for line in lines:
            result = pattern.search(line)
            if result is None:
                f.write(line)
            f.truncate()

    with open('access.txt', 'r+') as q:
        lines = q.readlines()
        q.seek(0)
        for line in lines:
            result = pattern.search(line)
            if result is None:
                q.write(line)
            q.truncate()

    with open('time.txt', 'r+') as w:
        lines = w.readlines()
        w.seek(0)
        for line in lines:
            result = pattern.search(line)
            if result is None:
                w.write(line)
            w.truncate()