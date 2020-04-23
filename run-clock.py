#!/usr/bin/env python3
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
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
        self.continumm = 0
        self.textColor = None

    def update_text_color(self):
        self.continumm += 1
        self.continumm %= 3 * 255

        red = 0
        green = 0
        blue = 0

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

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        stationary_font = graphics.Font()
        stationary_font.LoadFont("./fonts/helvR12.bdf")
        scrolling_font = graphics.Font()
        scrolling_font.LoadFont("./fonts/7x13B.bdf")
        self.update_text_color()
        stationary_pos = 0
        scrolling_pos = offscreen_canvas.width
        now = arrow.now()
        my_text = [f"{now.hour:02d}:{now.minute:02d}", f"{now.month:02d}/{now.day:02d}"]
        scrolling_text = ["Mischief Managed", "Hack the Planet!", "Do good."]
        st_len = len(scrolling_text)
        st_index = 0
        count = 0
        while True:
            offscreen_canvas.Clear()
            offset = 10
            for text in my_text:
                graphics.DrawText(
                    offscreen_canvas,
                    stationary_font,
                    stationary_pos,
                    offset,
                    self.textColor,
                    text,
                )
                offset += 10
            offset += 0
            new_pos = graphics.DrawText(
                offscreen_canvas,
                scrolling_font,
                scrolling_pos,
                offset,
                self.textColor,
                scrolling_text[st_index],
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
                    f"{now.hour:02d}:{now.minute:02d}",
                    f"{now.month:02d}/{now.day:02d}",
                ]

            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            self.update_text_color()


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if not run_text.process():
        run_text.print_help()
