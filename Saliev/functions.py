import numpy as np
import math
import sympy as sp


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


def multiple(a, b):    # Нахождение мультипликативной инверсии числа
    if math.gcd(a, b) == 1 and b != 0:
        b %= a
        t1, t2 = 0, 1

        while a != 1:
            q = a // b
            r = a % b
            t = t1 - (q * t2)
            t1 = t2
            t2 = t
            a = b
            b = r
        if t1 < 0:
            t1 += 26
        return t1
    else:
        return 0


def get_matrix_minor(m, i, j):  # Нахождение минора
    return [row[:j] + row[j + 1:] for row in (m[:i] + m[i + 1:])]


def det(matrix):    # Детерминант матрицы
    return sp.Matrix(matrix).det()


def txt_to_matrix(txt, key_length):     # Текст -> матрицу
    x = []
    for i in txt.upper():
        x.append(ord(i) - 65)
    y = [x[i:key_length + i] for i in range(0, len(x), key_length)]
    for j in y:
        if len(j) < key_length:
            for i in range(key_length - len(j)):
                j.append(0)
    return y


def key_to_matrix(key_text, key_length):    # Ключ текст -> Матрица
    key_text = key_text[:pow(key_length, 2)]
    matrix_key = []
    sr = []
    for i in key_text.upper():
        sr.append(ord(i) - 65)
        if len(sr) == key_length:
            matrix_key.append(sr)
            sr = []
    return matrix_key