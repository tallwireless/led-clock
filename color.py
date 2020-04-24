from rgbmatrix import graphics


class BaseColor(object):
    def __init__(self, red=0, green=0, blue=0):
        self.red = red
        self.blue = blue
        self.green = green
        self.textColor = graphics.Color(self.red, self.green, self.blue)

    def get_color(self):
        return self.textColor


class ColorContinium(BaseColor):
    def __init__(self, seed=0, speed=1):
        self.continumm = seed
        self.speed = speed
        self.textColor = None

    def update_color(self):
        self.continumm += self.speed
        self.continumm %= 3 * 255

        blue = 0
        red = 0
        green = 0

        if self.continumm <= 255:
            c = self.continumm
            blue = 255 - c
            red = c
        elif self.continumm > 255 and self.continumm <= 511:
            c = self.continumm - 256
            red = 255 - c
            green = c
        else:
            c = self.continumm - 512
            green = 255 - c
            blue = c
        self.textColor = graphics.Color(red, green, blue)

    def get_color(self):
        self.update_color()
        return self.textColor
