import random
#Image:一个画板(context), ImageDraw:一个画笔, ImageFont:画笔的字体
from PIL import Image, ImageDraw, ImageFont
import time
import os
import string

class Captcha(object):
    #字体的位置
    font_path = os.path.join(os.path.dirname(__file__), 'verdana.ttf')

    #生成几位数的验证码
    number = 4

    #生成验证码图片的宽度和高度
    size = (100, 40)

    #背景颜色默认为白色 RGB(Red, Green, Blue)
    bgcolor = (0, 0, 0)   #黑色

    #随机字体颜色
    random.seed(int(time.time()))
    fontcolor = (random.randint(200, 255), random.randint(100, 255), random.randint(100, 255))

    #验证码字体大小
    fontsize = 20

    #随机干扰线颜色
    linecolor = (random.randint(0, 250), random.randint(0, 255), random.randint(0, 250))

    #是否要加入干扰线
    draw_line = True

    #是否绘制干扰线
    draw_point = True

    #加入干扰线的条数
    line_number = 3


    #string.ascii_letters会生成 a-z,A-Z 的字符串
    SOURCE = list(string.ascii_letters)
    for index in range(0, 10):
        SOURCE.append(str(index))
    #现在的 SOURCE 是由 a-z.A-Z,0-9组成的字符串


    #定义私有类方法
    @classmethod
    def gene_text(cls):
        return ''.join(random.sample(cls.SOURCE, cls.number))  #生成验证码的字符串

    #绘制干扰线
    @classmethod
    def __gene_line(cls, draw, width, height):
        begin = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([begin, end], fill = cls.linecolor)

    #绘制干扰点
    @classmethod
    def __gene_points(cls, draw, point_chance, width, height):
        chance = min(100, max(0, int(point_chance)))
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill = (0, 0, 0))

    #生成验证码
    @classmethod
    def gene_code(cls):
        width, height = cls.size #宽和高
        image = Image.new('RGBA', (width, height), cls.bgcolor)  #创建画板
        font = ImageFont.truetype(cls.font_path, cls.fontsize)  #验证码字体
        draw = ImageDraw.Draw(image)  #创建画笔
        text = cls.gene_text()  #生成字符串
        font_width, font_height = font.getsize(text)
        draw.text(((width - font_width) / 2, (height - font_height) / 2), text, font=font, fill=cls.fontcolor)  #填充字符串

        #如果需要绘制干扰线
        if cls.draw_line:
            #遍历line_number次, 就是画line_number条线
            for x in range(0, cls.line_number):
                cls.__gene_line(draw, width, height)

        #如果需要绘制噪点
        if cls.draw_point:
            cls.__gene_points(draw, 10, width, height)

        return (text, image)