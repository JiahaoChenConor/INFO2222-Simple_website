from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
import random
import base64


# 验证码图片
def validate_picture():
    total = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ012345789'
    width = 130
    heighth = 50
    im = Image.new('RGB', (width, heighth), 'white')
    font = ImageFont.truetype("SourceSans3-Regular.ttf", 30)
    draw = ImageDraw.Draw(im)
    str = ''
    for item in range(4):
        text = random.choice(total)
        str += text
        draw.text((-3 + random.randint(3, 7) + 25 * item, -3 + random.randint(2, 7)), text=text, fill='black',
                  font=font)

    for num in range(1):
        x1 = random.randint(0, int(width / 2))
        y1 = random.randint(0, int(heighth / 2))
        x2 = random.randint(0, width)
        y2 = random.randint(int(heighth / 2), heighth)
        draw.line(((x1, y1), (x2, y2)), fill='black', width=1)

    im = im.filter(ImageFilter.FIND_EDGES)
    return im, str
