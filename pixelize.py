from PIL import Image
from math import sqrt

from colorthief import ColorThief


def pass_to_palette(rgb, palette):
    '''
        Метод для вибору відповідного кольору з палітри для вхідного кольору
    
        @params
            rgb      -  вхідний колір, кортеж виду (r, g, b)
            palette  -  палітра кольорів, для якої підпасовується вхідний колір
        
        @returns
            найближчий до вхідного колір, обраний з палітри
    '''

    input_brightness = calc_brightness(rgb)
    delta = 255
    passed_color = (0, 0, 0)

    for brightness in palette.keys():
        new_delta = abs(brightness - input_brightness) 
        if new_delta < delta:
            delta = new_delta
            passed_color = palette[brightness] 

    return passed_color


def color_avg(pixel_values):
    '''
        Знаходить середнє значення для списку вхідних RGB кольорів
        Джерело: sighack.com/post/averaging-rgb-colors-the-right-way

        @params
            pixel_values   -  список кортежів виду (r, g, b)

        @returns
            середнє арифметичне для списку вхідних кольорів

    '''
    
    r_total, g_total, b_total = 0, 0, 0
    amount = 0
    
    for value in pixel_values:
        r, g, b = value
        
        r_total += r**2
        g_total += g**2
        b_total += b**2

        amount += 1
    
    return (
            sqrt(r_total / amount),
            sqrt(g_total / amount),
            sqrt(b_total / amount)
    )


def pixelize(image, palette, pixel_size):
    '''
        Метод для пікселізації вхідного зображення 

        @params
            image      -  вхідне зображення
            palette    -  палітра кольорів
            pixel_size -  розмірність пікселя
    
        @returns
            пікселізоване зображення
    '''

    w, h = image.size

    w -=  w % pixel_size
    h -=  h % pixel_size

    pix_image = Image.new(
        mode='RGB', size=(w, h)
    )

    for i in range(0, w, pixel_size):
        for j in range(0, h, pixel_size):
            pixel_values = []
            for x in range(i, i + pixel_size):
                for y in range(j, j + pixel_size):
                    pixel_values.append(image.getpixel((x, y)))
            
            average = color_avg(pixel_values)
            r, g, b = pass_to_palette(average, palette)

            for x in range(i, i + pixel_size):
                for y in range(j, j + pixel_size):
                    pix_image.putpixel((x, y), (int(r), int(g), int(b), 255))

    return pix_image


def get_palette(path, palette_size):
    '''
        Метод для отримання палітри кольорів з фото за допомогою colorthief (стороння бібліотека)

        @params
            path          -  шлях до зображення, що є джерелом палітри
            palette_size  -  розмір палітри, що буде сформована

        @returns

    '''
    
    colors = ColorThief(path).get_palette(color_count=palette_size)

    palette = {}
    for color in colors:
       palette[round(calc_brightness(color))] = color
    return palette


def calc_brightness(rgb):
    '''
        Метод для знаходження яскравості кольору

        @params
            rgb - вхідний колір, кортеж виду (r, g, b)

        @returns
            значення яскравості для вхідного кольору 

    '''

    r, g, b = rgb
    return sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2))
