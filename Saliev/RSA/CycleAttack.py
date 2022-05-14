ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def to_str(c_text):
    if len(c_text) % 2 == 1:
        c_text = '0' + c_text
    re = ''
    for i in range(0, len(c_text), 2):
        qw = int(c_text[i:i+2])
        re += ALPHABET[qw]
    return re


i = True
z = 0
C = int(input("Введите шифротекст C: "))
n = int(input("Введите модуль n: "))
e = int(input("Введите e: "))
X = 1
X = C
while i:
    Y = C            # Присваиваем предыдущий ответ С
    C = pow(C, e, n) # Возводим в степень
    if X == C:
        i = False
        print(Y)
        print(to_str(str(Y)))