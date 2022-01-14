import numpy as np
from functions import det, txt_to_matrix, key_to_matrix, multiple


def encryption(i_text, txt_key, dl_key):    # функция для шифрования текста

    matrix_key = key_to_matrix(txt_key, dl_key)  # Текст-ключ -> матрица
    det_m = int(det(matrix_key))    # нахождение детерминанта матрицы
    mul = multiple(26, det_m % 26)  # нахождение мультипликативную инверсию

    while mul == 0:     # Цикл while - добавляет букву "б" на начало текста. Пока не найдет мультипликативную обратную

        txt_key = "b" + txt_key     # Добавление "б"
        matrix_key = key_to_matrix(txt_key, dl_key)    # Текст-ключ -> матрица
        det_m = int(det(matrix_key))        # нахождение детерминанта матрицы
        mul = multiple(26, det_m % 26)      # нахождение мультипликативную инверсию

    txt_2_matrix = txt_to_matrix(i_text, dl_key)   # Превращает текст в матрицу

    result = (np.array(txt_2_matrix).dot(np.array(matrix_key))) % 26    # Шифрование

    qw = []
    for i in txt_2_matrix:
        we = []
        for j in i:
            we.append(chr(j+97))
        qw.append(we)

    print(qw)

    c_txt = ''                  #
    for i in result:            #
        for j in i:             # -> array to str
            res = chr(j+65)     #
            c_txt += res        #

    return f'Шифрованный текст: {c_txt}'    # Возвращает зашифрованный текст


def decryption(cipher_text, key_1, key_length):     # Функция для расшифровки

    matrix_key = key_to_matrix(key_1, key_length)  # Текст-ключ -> матрица
    det_m = int(det(matrix_key))    # нахождение детерминанта матрицы
    mul = multiple(26, det_m % 26)  # нахождение мультипликативную инверсию

    while mul == 0:
        key_1 = "b" + key_1
        matrix_key = key_to_matrix(key_1, key_length)
        det_m = int(det(matrix_key))
        mul = multiple(26, det_m % 26)

    cipher_txt_2_matrix = txt_to_matrix(cipher_text, key_length)  # Превращает текст в матрицу

    inv = (((np.linalg.inv(matrix_key) * det_m) % 26) * mul) % 26   # Нахождение обратной матрицы
    res = np.around(np.dot(matrix_key, inv) % 26).astype(int) % 26  # Умножение обратной матрицы с исходной. Чтобы проверить правильно ли нашел

    result = np.allclose(res, np.eye(np.array(matrix_key).shape[0]))    # Проверка на правильность. Если правильно возвращает True

    if result:  # Если result True
        final = np.around(np.dot(cipher_txt_2_matrix, inv) % 26).astype(int) % 26   # То происходит расшифровка

        dec_txt = ''                            # \
        for i in final:                         # _\
            for j in i:                         # - > Перевод рашифрованную матрицу в текст
                dec_txt += chr(j+65).lower()    # _/
        return dec_txt                          # /
    else:
        return 0


def attack(text, cliper_text):
    length = len(cliper_text)
    roz = length - len(text)
    text = text + ('a' * roz)
    print(text)

    deliteli = []
    for i in range(2, length, 1):
        if length % i == 0:
            deliteli.append(i)
    q = []
    for j in deliteli:
        print(j)
        text_m = txt_to_matrix(text, j)  # Text -> Matrix
        c_t_m = txt_to_matrix(cliper_text, j)
        det_m = int(det(text_m))  # нахождение детерминанта матрицы
        mul = multiple(26, det_m % 26)  # нахождение мультипликативную инверсию

        inv = (((np.linalg.inv(text_m) * det_m) % 26) * mul) % 26  # Нахождение обратной матрицы
        res = np.around(np.dot(inv, text_m) % 26).astype(int) % 26  # Умножение обратной матрицы с исходной. Чтобы проверить правильно ли нашел
        result = np.allclose(res, np.eye(np.array(text_m).shape[0]))  # Проверка на правильность. Если правильно возвращает True

        if result:  # Если result True
            final = np.around((np.dot(inv, c_t_m) % 26)).astype(int)  # То происходит расшифровка
            f = np.around(np.dot(np.array(c_t_m), np.array([list(i) for i in zip(*final)]))).astype(int) % 26
            print(f)

            c_txt = ''  #
            for i in final:  #
                for j in i:  # -> array to str
                    res = chr(j + 65)  #
                    c_txt += res
            print(c_txt)
            q.append(final)

        else:
            print(0)
            q.append(0)
    print(q)


choose = int(input("1 - Шифрование\n2 - Расшифрование\nВаш выбор: "))
if choose == 1:
    text = input('Введите текст: ')
    d_key = int(input('Введите размер ключа: '))
    key = input('Введите ключ-текст: ')
    print(encryption(text, key, d_key))
elif choose == 2:
    text = input('Введите шифро-текст: ')
    d_key = int(input('Введите размер ключа: '))
    key = input('Введите ключ-текст: ')
    q = decryption(text, key, d_key)
else:
    text = input('Введите шифро-текст: ')
    text2 = input('Введите исходный текст: ')
    q = attack(text2, text)
    print(q)