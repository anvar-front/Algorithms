import math
import time


def IsPrime(n):
    d = 2
    while d * d <= n and n % d != 0:
        d += 1
    return d * d > n


n = int(input("Введите модуль: "))
r = []
sq = math.sqrt(n)
s = 0
start_time = time.time()
for i in range(int(sq), 1, -1):
    if IsPrime(i):
        s += 1
        if math.floor(n/i) == n/i:
            print(i, int(n/i))

# print(s, '\n')
print("--- %s секунд ---" % (time.time()-start_time))
