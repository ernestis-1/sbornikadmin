from PIL import Image
print("Изображение - море")
im = Image.open(r'C:\Users\eivan\Desktop\sea.jpg')
# Откроет изображение в новом окне
im.show()

im1 = Image.new('RGB', (200,200), color=('#FAACAC'))
# Откроет изображение в новом окне
im1.show()
