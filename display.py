from samplebase import SampleBase
import time


class Display(SampleBase):
    def __init__(self, *args, **kwargs):
        super(Display, self).__init__(*args, **kwargs)
        self.parser.add_argument(
            "-t",
            "--text",
            help="The text to scroll on the RGB LED panel",
            default="Hello world!",
        )
        self.elements = []

    def registerElement(self, element):
        element.registerDisplay(self)
        self.elements.append(element)

    def run(self):
        canvas = self.matrix.CreateFrameCanvas()
        count = 0
        while True:
            canvas.Clear()
            offset = 0
            for element in self.elements:
                offset += element.height
                element.draw(canvas, offset)
                offset += 1
            time.sleep(0.03)
            count += 1
            if count % 20 == 0:
                for element in self.elements:
                    element.update()
                count = 0
            canvas = self.matrix.SwapOnVSync(canvas)
