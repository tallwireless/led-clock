#!/usr/bin/env python3
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
from color import ColorContinium
import time
import arrow


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
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        stationary_font = graphics.Font()
        stationary_font.LoadFont("./fonts/helvR12.bdf")
        scrolling_font = graphics.Font()
        scrolling_font.LoadFont("./fonts/7x13B.bdf")
        stationary_pos = 0
        scrolling_pos = offscreen_canvas.width
        now = arrow.now()
        my_text = [
            [f"{now.hour:02d}:{now.minute:02d}", ColorContinium(120, -3)],
            [f"{now.month:02d}/{now.day:02d}", ColorContinium(200, 3)],
        ]
        scrolling_text = [
            ["Hi Kevin!", ColorContinium(45, 20)],
            ["This is sample text that's really long", ColorContinium(150, 6)],
            ["Goodbye.", ColorContinium(250, 6)],
        ]
        st_len = len(scrolling_text)
        st_index = 0
        count = 0

        while True:
            offscreen_canvas.Clear()
            offset = 10
            for (text, color) in my_text:
                graphics.DrawText(
                    offscreen_canvas,
                    stationary_font,
                    stationary_pos,
                    offset,
                    color.get_color(),
                    text,
                )
                offset += 10
            offset += 0
            new_pos = graphics.DrawText(
                offscreen_canvas,
                scrolling_font,
                scrolling_pos,
                offset,
                scrolling_text[st_index][1].get_color(),
                scrolling_text[st_index][0],
            )
            scrolling_pos -= 1

            if scrolling_pos + new_pos < 0:
                st_index += 1
                if st_index >= st_len:
                    st_index = 0
                scrolling_pos = offscreen_canvas.width

            time.sleep(0.05)
            count += 1
            if count % 20 == 0:
                now = arrow.now()
                my_text = [
                    [f"{now.hour:02d}:{now.minute:02d}", my_text[0][1]],
                    [f"{now.month:02d}/{now.day:02d}", my_text[1][1]],
                ]

            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if not run_text.process():
        run_text.print_help()
