from functions import *


def encryption(txt, key):
    length = len(key)
    matrix_key = [[0 for x in range(length)] for y in range(length)]

    for i, j in enumerate(key):
        matrix_key[i][j-1] = 1

    res = [list(i) for i in zip(*matrix_key)]

    text_m = txt_to_matrix(txt, length)        # Text -> Matrix

    result = np.array(text_m).dot(np.array(res))

    c_txt = ''  #
    for i in result:  #
        for j in i:  # -> array to str
            res = chr(j + 65)  #
            c_txt += res  #

    return f'Шифрованный текст: {c_txt}'  # Возвращает зашифрованный текст


def decryption(txt, key):
    length = len(key)
    matrix_key = [[0 for x in range(length)] for y in range(length)]

    for i, j in enumerate(key):
        matrix_key[i][j - 1] = 1

    text_m = txt_to_matrix(txt, length)  # Text -> Matrix

    result = np.array(text_m).dot(np.array(matrix_key))

    c_txt = ''  #
    for i in result:  #
        for j in i:  # -> array to str
            res = chr(j + 65)  #
            c_txt += res  #

    return f'Шифрованный текст: {c_txt}'  # Возвращает зашифрованный текст


def attack(text, cliper_text):
    length = len(cliper_text)
    roz = length - len(text)
    text = text + ('a'*roz)

    deliteli = []
    for i in range(2, length, 1):
        if length % i == 0:
            deliteli.append(i)
    q = []
    for j in deliteli:

        text_m = txt_to_matrix(text, j)  # Text -> Matrix
        c_t_m = txt_to_matrix(cliper_text, j)
        det_m = int(det(text_m))  # нахождение детерминанта матрицы
        mul = multiple(26, det_m % 26)  # нахождение мультипликативную инверсию

        inv = (((np.linalg.inv(text_m) * det_m) % 26) * mul) % 26   # Нахождение обратной матрицы

        res = np.around(np.dot(text_m, inv) % 26).astype(int) % 26  # Умножение обратной матрицы с исходной. Чтобы проверить правильно ли нашел
        result = np.allclose(res, np.eye(np.array(text_m).shape[0]))  # Проверка на правильность. Если правильно возвращает True

        if result:  # Если result True
            final = (np.dot(inv, c_t_m) % 26)  # То происходит расшифровка
            f = np.around(np.dot(np.array(c_t_m), np.array([list(i) for i in zip(*final)]))).astype(int) % 26
            print(f)
            q.append(final)

        else:
            print(0)
    return q


choice = int(input("1 - Шифрование, 2 - Расшифрование, 3 - Атака по образцу\nВаш выбор: "))
if choice == 1:
    i = [int(a) for a in input('Введите ключ: ').split()]
    text = input("Введите текст: ")
    result = encryption(text, i)
    print(result)

elif choice == 2:
    i = [int(a) for a in input('Введите ключ: ').split()]
    text = input("Введите текст: ")
    result = decryption(text, i)
    print(result)

elif choice == 3:
    text = input("Введите исходный текст: ")
    text_2 = input("Введите шифрованный текст: ")
    result = attack(text, text_2)
    print(result)