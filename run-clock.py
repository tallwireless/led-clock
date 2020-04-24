#!/usr/bin/env python3
# Display a runtext with double-buffering.
from samplebase import SampleBase
from color import ColorContinium, BaseColor
from line import ScrollingLine, DateTimeLine
import time


class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument(
            "-t",
            "--text",
            help="The text to scroll on the RGB LED panel",
            default="Hello world!",
        )

    def run(self):
        lines = [
            DateTimeLine(
                color=ColorContinium(120, -3),
                font="./fonts/helvR12.bdf",
                fmt="%H:%Y",
                height=9,
            ),
            DateTimeLine(
                color=ColorContinium(240, 3),
                font="./fonts/helvR12.bdf",
                fmt="%m/%d",
                height=9,
            ),
            ScrollingLine(
                text="Look Ma! I'm scrolling!",
                color=BaseColor(255, 0, 255),
                font="./fonts/7x13B.bdf",
                height=10,
            ),
        ]
        canvas = self.matrix.CreateFrameCanvas()
        count = 0
        while True:
            canvas.Clear()
            offset = 0
            for line in lines:
                offset += line.height
                line.draw(canvas, offset)
                offset += 1
            time.sleep(0.05)
            count += 1
            if count % 20 == 0:
                for line in lines:
                    line.update
                count = 0
            canvas = self.matrix.SwapOnVSync(canvas)


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if not run_text.process():
        run_text.print_help()
