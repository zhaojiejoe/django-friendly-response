from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
from io import BytesIO
import pathlib

TTF_PATH = pathlib.PurePath(__file__).parent

class ValidationCodeImageService():
    """
    default width:200, height:38px;
    default background color white;
    """
    # chars = '234567890ABCDEFGHJKLMNOPQRSTUVWXY234567890abcdefghijkmnopqrstuvwxy234567890'
    # 避免以下字符：
    # 1, 0, 大小写o，小写l，大写I
    # chars = '23456789ABCDEFGHJKLMNPQRSTUVWXYabcdefghijkmnpqrstuvwxyz'
    # 进一步简化验证码
    chars = '1234567890'

    def __init__(self, width=120, height=40, mode='RGB', str_length=4):
        self.width = width
        self.height = height
        self.mode = mode
        self.str_length = str_length

    def get_chars(self, length):
        """
        生成给定长度的字符串，返回列表格式
        """
        return random.sample(self.chars, length)

    def create_strs(self):
        """
        绘制验证码字符
        """
        c_chars = self.get_chars(self.str_length)
        strs = '%s' % ''.join(c_chars)

        return strs

    def get_random_color(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return (r, g, b)

    def draw_line(self, draw):
        for i in range(3):
            x1 = random.randint(0, self.width)
            x2 = random.randint(0, self.width)
            y1 = random.randint(0, self.height)
            y2 = random.randint(0, self.height)
            draw.line((x1, y1, x2, y2), fill=self.get_random_color())

    def draw_point(self, draw):
        for i in range(50):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            draw.point((x,y), fill=self.get_random_color())


    def draw_image(self):
        size = (self.width, self.height)
        image = Image.new(self.mode, size, (255, 255, 255))
        draw = ImageDraw.Draw(image)
        strs = self.create_strs()
        font = ImageFont.truetype(str(pathlib.Path(TTF_PATH, 'simfang.ttf')), 24)
        font_width, font_height = font.getsize(strs)
        draw.text(((self.width - font_width) / 3, (self.height - font_height) / 4),
                  strs, font=font, fill=(0, 0, 0))
        self.draw_point(draw)
        self.draw_line(draw)
        params = [1 - float(random.randint(1, 2)) / 100,
                  0,
                  0,
                  0,
                  1 - float(random.randint(1, 10)) / 100,
                  float(random.randint(1, 2)) / 500,
                  0.001,
                  float(random.randint(1, 2)) / 500
        ]
        image = image.transform(size, Image.PERSPECTIVE, params) # 创建扭曲
        image = image.filter(ImageFilter.EDGE_ENHANCE) # 滤镜，边界加强（阈值更大）
        return image, strs


if __name__ == '__main__':
    vcis = ValidationCodeImageService()
    img, strs = vcis.draw_image()
    buf = BytesIO()
    img.save(buf, 'JPEG', quality=70)
    print(strs)
