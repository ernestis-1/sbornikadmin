from PIL import Image, ImageDraw, ImageFont

print("Введите путь изображения")
p=str(input())
im = Image.open(p)
#im = Image.open(r'C:\Users\eivan\Desktop\sea.jpg')#нужно выбрать неоюходимый файл
draw_text = ImageDraw.Draw(im)

print("Введите текст, который должен быть на изображении")
t=str(input())
print("Введите координаты текста на изображении(2 положительных целых числа)")
x=int(input())
y=int(input())
draw_text.text(
    (x,y),
    t,
    fill=('#1C0606')
    )
im.show()

