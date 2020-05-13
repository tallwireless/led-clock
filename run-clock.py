#!/usr/bin/env python3
# Display a runtext with double-buffering.
from samplebase import SampleBase
from color import ColorContinium, BaseColor
from line import ScrollingLine, DateTimeLine, MultiScrollingLine
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


# Main function
if __name__ == "__main__":
    display = Display()
    display.registerElement(
        DateTimeLine(
            color=BaseColor(255, 0, 0),
            font="./fonts/helvR12.bdf",
            fmt="%H:%M",
            height=9,
            align="center",
        )
    )
    display.registerElement(
        DateTimeLine(
            color=ColorContinium(240, 3),
            font="./fonts/helvR12.bdf",
            fmt="%m/%d/%y",
            height=9,
            align="center",
        )
    )

    scrolling = MultiScrollingLine()
    scrolling.addMessage(
        ScrollingLine(
            text="I solemnly swear I'm up to no good.",
            color=ColorContinium(3, -48),
            font="./fonts/7x13B.bdf",
            height=10,
        )
    )
    scrolling.addMessage(
        ScrollingLine(
            text="Do your best, good sir.",
            color=ColorContinium(234, -12),
            font="./fonts/7x13B.bdf",
            height=10,
        )
    )
    scrolling.addMessage(
        ScrollingLine(
            text="Mischief managed.",
            color=ColorContinium(234, -12),
            font="./fonts/7x13B.bdf",
            height=10,
        )
    )
    display.registerElement(scrolling)
    if not display.process():
        display.print_help()
