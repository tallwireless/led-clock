#!/usr/bin/env python3
# Display a runtext with double-buffering.
from color import ColorContinium, BaseColor
from line import ScrollingLine, DateTimeLine, MultiScrollingLine
from display import Display

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
