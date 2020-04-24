#!/usr/bin/env python3
# Display a runtext with double-buffering.
from samplebase import SampleBase
from color import ColorContinium
from line import ScrollingLine, DateTimeLine, MultiScrollingLine
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
                fmt="%H:%M",
                height=9,
            ),
            DateTimeLine(
                color=ColorContinium(240, 3),
                font="./fonts/helvR12.bdf",
                fmt="%m/%d",
                height=9,
            ),
            MultiScrollingLine(),
        ]
        lines[2].addMessage(
            ScrollingLine(
                text="I solemnly swear I'm up to no good.",
                color=ColorContinium(3, -10),
                font="./fonts/7x13B.bdf",
                height=10,
            )
        )
        lines[2].addMessage(
            ScrollingLine(
                text="Do your best, good sir.",
                color=ColorContinium(234, 5),
                font="./fonts/7x13B.bdf",
                height=10,
            )
        )
        lines[2].addMessage(
            ScrollingLine(
                text="Mischief managed.",
                color=ColorContinium(234, -12),
                font="./fonts/7x13B.bdf",
                height=10,
            )
        )
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
                    line.update()
                count = 0
            canvas = self.matrix.SwapOnVSync(canvas)


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if not run_text.process():
        run_text.print_help()
