import os
from openpyxl import load_workbook

ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def text_int(txt):
    res = ''
    for i in txt:
        if ALPHABET.index(i) < 10:
            res += '0' + str(ALPHABET.index(i))
        else:
            res += str(ALPHABET.index(i))
    return int(res)


def to_bin(c_key):
    resul = ''
    while c_key:
        resul += str(c_key % 2)
        c_key = c_key // 2
    return resul


def p_mod(txt, c_key, m):
    r = []
    first = (1*txt) % module
    r.append(first)
    for i in range(len(c_key)-1):
        r.append((r[-1]**2) % m)
    finish = 1
    for i in range(len(c_key)):
        if c_key[i] == '1':
            finish *= r[i]
    return finish % m


def to_str(c_text):
    re = ''
    for i in range(0, len(c_text), 2):
        qw = int(c_text[i:i+2])
        re += ALPHABET[qw]
    return re


def encryption(txt, c_key, m):
    first = text_int(txt)                   # translate str to int -> "no" = 1314
    second = to_bin(c_key)                  # translate key to binary -> 343 = 111010101
    third = p_mod(first, second, m)         # encrypt
    return third


def decryption(txt, c_key, m):
    first = to_bin(c_key)                   # translate key to binary -> 12007 = 11100111011101
    second = p_mod(txt, first, m)           # decrypt
    return str(second)


if __name__ == '__main__':
    choice = int(input("1 - encryption\n2 - decryption\n3 - quit\nYour choice: "))
    while choice != 3:
        if choice == 1:
            text = input("Input your plain text: ")
            key = int(input("Input your public key: "))
            module = int(input("Input module: "))
            res = encryption(text, key, module)

            wb = load_workbook('cipher.xlsx')
            ws = wb['data']
            ws.append([text, res])
            wb.save('cipher.xlsx')
            wb.close()

            # with open('/Users/anvar/PycharmProjects/RSA/text.txt', 'a') as file:
            #     res = encryption(text, key, module)
            #     file.write(f'{text}\t\t\t\t\t{res}')
            #     file.close()
            print("Cipher text recorded to text.xlsx file")
        elif choice == 2:
            text = int(input("Input your cipher text: "))
            key = int(input("Input your private key: "))
            module = int(input("Input module: "))
            q = decryption(text, key, module)
            print(f'Plain text - {to_str(q)}')
        elif choice == 3:
            print('Good luck!')
        ch = input('Do you want to continue? (y/n): ')
        if ch == 'y':
            os.system('clear')
        else:
            exit()
        choice = int(input("1 - encryption\n2 - decryption\n3 - quit\nYour choice: "))
