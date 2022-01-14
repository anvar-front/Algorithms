import numpy as np
import math
from functions import multiple, encryption

alphabet = 'abcdefghijklmnopqrstuvwxyz'
len_alpha = len(alphabet)


def additive(a):    # Нахождение аддитивной инверсии числа
    return len_alpha - a


def decryption(Text, m_key, a_key):    # Расшифровка текста
    result = ''
    for word in Text:
        i_word = ord(word) - 65
        c = (((i_word+additive(a_key)) % len_alpha) * multiple(len_alpha, m_key)) % len_alpha

        res = chr(c + 65)
        result += res
    return result.lower()


def pattern_attack(Text, i_t, s_t):    # Атака по образцу
    res = ''
    i_array = np.array([[ord(i)-97, 1] for i in list(i_t[:2])])
    o_array = np.array([[ord(i)-97, 1] for i in list(i_t[:2])])
    s_array = np.array([[ord(i)-65] for i in list(s_t[:2])])

    o_array[0][0], o_array[1][1] = -(o_array[1][1]), -(o_array[0][0])
    e = np.dot(i_array, o_array)

    ed_array = [[1, 0] for i in range(2)]
    ed_array[1][0], ed_array[1][1] = ed_array[1][1], ed_array[1][0]

    if np.allclose(e, ed_array):
        k = o_array.dot(s_array)
        multiple_key = multiple(len_alpha, k[0][0])
        additive_key = additive(k[1][0])

        for i in Text:
            c = (((ord(i)-65) + additive_key)*multiple_key) % len_alpha
            r = chr(c+65)
            res += r

        return res
    return 'Текст зашифрован неправильно'


choice = int(input("1 - Зашифровать\n2 - Расшифровать\n3 - Атака\nВыберите один вариант: "))
if choice == 1:

    plainText = input("Enter the text: ")
    text = "".join(plainText.split())
    text_1 = "".join([chr(ord(i)-32) if 97 <= ord(i) <= 122 else i for i in text])
    multiple_key = int(input('enter the multiply key: '))

    add_key = int(input('enter the additive key: '))

    cipher_text = encryption(text_1, multiple_key, add_key)
    print(f'Encryption text: {cipher_text}')

elif choice == 2:
    plainText = input("Enter the text: ")
    multiple_key = int(input('enter the multiply key: '))
    add_key = int(input('enter the additive key: '))
    cipher_text = decryption(plainText, multiple_key, add_key)
    print(f'Decryption text: {cipher_text}')
else:
    choice_2 = int(input('1 - Атака грубой силой\n2 - Атака по образцу\nВыберите один вариант: '))
    if choice_2 == 1:

        plainText = input("Enter the text: ")
        mul = []
        for i in range(len_alpha):
            mul.append(multiple(len_alpha, i))
        mul = sorted([i for i in mul if i != 0])
        print(mul)

        for i in mul:
            for j in range(len_alpha):
                w = decryption(plainText, i, j)
                print(w, i, j)
    else:
        txt = input('Введите зашифрованный текст: ')
        i_txt = input('Введите исходные буквы: ')
        s_txt = input('Введите зашифрованные буквы: ')
        print((pattern_attack(txt, i_txt, s_txt)).lower())