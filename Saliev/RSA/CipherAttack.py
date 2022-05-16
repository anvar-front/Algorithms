import math

ALPHABET = "abcdefghijklmnopqrstuvwxyz"


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


e = int(input("Введите открытый ключ: "))
C = int(input("Введите зашифрованный текст: "))
n = int(input("Введите модуль: "))
d = int(input("d? "))


print("Этап Евы")

i = 0
while i == 0:
    X = int(input("Введите X для шифрования: "))
    res = multiple(X, n)
    if res != 0:
        i = 1

C1 = pow(X, e, n)   # Ева шифрует Х и передает Бобу
print(C1)
y = (C * C1) % n #начальный шифр
print('y: ', y)

print("Ева дает расшифровать",y)
Z = pow(y,d,n) # даем на дешифрацию
print(Z)

print('Боб дает Еве: ',Z)

P = (Z*multiple(n,X))%n
print(P)