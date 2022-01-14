import os
import sys

HEADER = 54


def start():
    choice = int(input('1 - Шифрование\n2 - Дешифрование\n3 - Выход\nВаш выбор? -> '))
    if choice == 1:
        input_img = input("Введите путь изображения: ")
        output_img = input("Введите название для изображения: ")
        txt_file = input("Введите путь текстового файла: ")
        degree = int(input("Введите количество байт для шифрования: "))
        encode(input_img, output_img, txt_file, degree)
    elif choice == 2:
        input_img = input("Введите путь изображения: ")
        output_txt = input("Введите название для текстового файла: ")
        degree = int(input("Введите количество байт для шифрования: "))
        file = open('tx.txt', 'r')
        data = file.read()
        symbols_to_read = len(data)
        decode(input_img, output_txt, symbols_to_read, degree)
    elif choice == 3:
        quit()
    else:
        print('Такого пункта не существует')
        quit()


def encode(input_img_name, output_img_name, txt_file, degree):
    if degree not in [1, 2, 4, 8]:
        print("Степень должен быть выбран из 1/2/4/8")
        return False

    text_len = os.stat(txt_file).st_size
    img_len = os.stat(input_img_name).st_size

    if text_len >= img_len * degree / 8 - HEADER:
        print("Слишком длинный текст")
        return False

    text = open(txt_file, 'r')
    input_image = open(input_img_name, 'rb')
    output_image = open(output_img_name, 'wb')

    bmp_header = input_image.read(HEADER)
    output_image.write(bmp_header)

    text_mask, img_mask = masks(degree)

    while True:
        symbol = text.read(1)
        if not symbol:
            break
        symbol = ord(symbol)

        for byte_amount in range(0, 8, degree):
            img_byte = int.from_bytes(input_image.read(1), sys.byteorder) & img_mask
            bits = symbol & text_mask
            bits >>= (8 - degree)
            img_byte |= bits

            output_image.write(img_byte.to_bytes(1, sys.byteorder))
            symbol <<= degree

    output_image.write(input_image.read())

    text.close()
    input_image.close()
    output_image.close()

    return True


def decode(encoded_img, output_txt, symbols_to_read, degree):
    if degree not in [1, 2, 4, 8]:
        print("Степень должен быть выбран из 1/2/4/8")
        return False

    img_len = os.stat(encoded_img).st_size

    if symbols_to_read >= img_len * degree / 8 - HEADER:
        print("Слишком длинный текст")
        return False

    text = open(output_txt, 'w', encoding='utf-8')
    encoded_bmp = open(encoded_img, 'rb')

    encoded_bmp.seek(HEADER)

    _, img_mask = masks(degree)
    img_mask = ~img_mask

    read = 0
    while read < symbols_to_read:
        symbol = 0

        for bits_read in range(0, 8, degree):
            img_byte = int.from_bytes(encoded_bmp.read(1), sys.byteorder) & img_mask
            symbol <<= degree
            symbol |= img_byte

        if chr(symbol) == '\n' and len(os.linesep) == 2:
            read += 1

        read += 1
        text.write(chr(symbol))

    text.close()
    encoded_bmp.close()
    return True


def masks(degree):
    text_mask = 0b11111111
    img_mask = 0b11111111

    text_mask <<= (8 - degree)
    text_mask %= 256
    img_mask >>= degree
    img_mask <<= degree

    return text_mask, img_mask


start()