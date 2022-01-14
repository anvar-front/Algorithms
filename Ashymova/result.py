from tkinter import *
from tkinter import ttk
from PIL import Image, ImageDraw
from random import randint
from re import findall


def StegaEncrypt(image, teext):
    img = Image.open(image)
    draw = ImageDraw.Draw(img)
    width = img.size[0]
    height = img.size[1]
    pix = img.load()
    f = open('key.txt', 'w')

    for elem in ([ord(elem) for elem in teext]):
        key = (randint(1, width - 10), randint(1, height - 10))
        g, b = pix[key][1:3]
        draw.point(key, (elem, g, b))
        f.write(str(key) + '\n')

    print('keys were written to the key.txt file')
    img.save("image.png", "PNG")
    f.close()


def StegaDecrypt(image, keyy):
    a = []
    keys = []
    img = Image.open(image)
    pix = img.load()
    f = open(keyy,'r')
    y = str([line.strip() for line in f])

    for i in range(len(findall(r'\((\d+)\,', y))):
        keys.append((int(findall(r'\((\d+)\,', y)[i]), int(findall(r'\,\s(\d+)\)', y)[i])))
    for key in keys:
        a.append(pix[tuple(key)][0])
    return ''.join([chr(elem) for elem in a])


def clicked():
    res = StegaEncrypt(cp.get(), txt_inp.get())
    out.configure(text='Ваш текст зашифрован')
    return res


def clicked2():
    res = StegaDecrypt(cp2.get(), txt_inp2.get())
    out2.configure(text='anvar')
    return res



window = Tk()
window.title("My application")
window.geometry('400x270')
tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Шифрование')
tab_control.add(tab2, text='Дешифрование')
lbl1 = Label(tab1, text='Введите путь исходной картинки', background='peach puff', width=30)
lbl1.grid(column=0, row=0)

cp = Entry(tab1, width=30)
cp.grid(column=0, row=2)

txt = Label(tab1, text='Введите текст', background='peach puff', width=30)
txt.grid(column=0, row=4)
txt_inp = Entry(tab1, width=30)
txt_inp.grid(column=0, row=6)

out = Label(tab1, text='', background='peach puff', width=30)
out.grid(column=0, row=11)

btn = Button(tab1, text='Зашифровать', command=clicked)
btn.grid(column=0, row=8)
# TAB 2
lbl2 = Label(tab2, text='Введите путь зашифрованной картинки', width=30, background='peach puff')
lbl2.grid(column=0, row=0)

cp2 = Entry(tab2, width=30)
cp2.grid(column=0, row=2)

txt2 = Label(tab2, text='Введите путь ключа', background='peach puff', width=30)
txt2.grid(column=0, row=4)
txt_inp2 = Entry(tab2, width=30)
txt_inp2.grid(column=0, row=6)

out2 = Label(tab2, text='', background='peach puff', width=30)
out2.grid(column=0, row=11)

btn2 = Button(tab2, text='Дешифровать', command=clicked2)
btn2.grid(column=0, row=8)

tab_control.pack(expand=1, fill='both')
window.mainloop()