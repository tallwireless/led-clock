import arrow
from rgbmatrix import graphics
from color import BaseColor


class TextLineException(Exception):
    pass


class TextLine(object):
    def __init__(self, *args, **kwargs):
        if "color" in kwargs:
            self.color = kwargs["color"]
        else:
            self.color = BaseColor(255, 255, 255)

        if "pos" in kwargs:
            self.pos = kwargs.pos
        else:
            self.pos = 0

        if "font" not in kwargs:
            raise TextLineException("Missing Font")
        self.font = graphics.Font()
        self.font.LoadFont(kwargs["font"])

        if "height" in kwargs:
            self.height = kwargs["height"]
        else:
            self.height = self.font.height

        if "align" in kwargs:
            self.align = kwargs["align"]
        else:
            self.align = "left"

        if "text" in kwargs:
            self.text = kwargs["text"]
        else:
            self.text = ""

        self.alignText()
        self.display = None

    def alignText(self):
        s = 0
        for char in self.text:
            s += self.font.CharacterWidth(ord(char))
        if self.align == "center":
            self.pos = int((64 - s) / 2)
        if self.align == "right":
            self.pos = 64 - s
        if self.align == "left":
            self.pos = 0

    def setText(self, text):
        """ Set the value of the text """
        self.text = text
        self.alignText()

    def draw(self, canvas, offset):
        return graphics.DrawText(
            canvas, self.font, self.pos, offset, self.color.get_color(), self.text
        )

    def registerDisplay(self, display):
        self.display = display

    def update(self):
        pass


class DateTimeLine(TextLine):
    """Prints out the data in the MM/DD format"""

    def __init__(self, *args, **kwargs):
        super(DateTimeLine, self).__init__(*args, **kwargs)
        if "fmt" in kwargs:
            self.fmt = kwargs["fmt"]
        else:
            self.fmt = "%H:%M %m/%d"
        self.update()

    def update(self):
        self.setText(arrow.now().strftime(self.fmt))


class ScrollingLine(TextLine):
    """ Prints Scrolling Text on the screen """

    def __init__(self, *args, **kwargs):
        super(ScrollingLine, self).__init__(*args, **kwargs)
        self.firstTime = True
        self.canvas_width = 0
        self.completed = False

    def draw(self, canvas, offset):
        if self.firstTime is True:
            self.pos = canvas.width
            self.canvas_width = canvas.width
            self.firstTime = False

        if self.completed:

            self.pos = self.canvas_width
            self.completed = False

        end_pos = super(ScrollingLine, self).draw(canvas, offset)
        self.pos -= 1

        if self.pos + end_pos <= 0:
            self.completed = True

        return end_pos


class MultiScrollingLine(object):
    def __init__(self, *args, **kwargs):
        self.firstTime = True
        self.canvas_width = 0
        self.messages = []
        self.height = 10
        self.mpos = 0

    def registerDisplay(self, display):
        pass

    def addMessage(self, message):
        self.messages.append(message)

    def draw(self, canvas, offset):
        if len(self.messages) == 0:
            raise MultiScrollingLineException("No ScrollingLine's Register")
        end_pos = self.messages[self.mpos].draw(canvas, offset)
        if self.messages[self.mpos].completed:
            self.mpos += 1
            if self.mpos >= len(self.messages):
                self.mpos = 0
        return end_pos

    def update(self):
        for message in self.messages:
            message.update()


class MultiScrollingLineException(Exception):
    pass
