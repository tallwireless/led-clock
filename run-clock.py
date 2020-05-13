#!/usr/bin/env python3
# Display a runtext with double-buffering.
from color import ColorContinium, BaseColor
from line import ScrollingLine, DateTimeLine, MultiScrollingLine
from display import Display
from screen import Screen

# Main function
if __name__ == "__main__":
    display = Display()
    screen1 = Screen()
    timeline = DateTimeLine(
        color=BaseColor(255, 0, 0),
        font="./fonts/helvR12.bdf",
        fmt="%H:%M",
        height=10,
        align="center",
    )
    screen1.registerElement(timeline)
    screen1.registerElement(
        DateTimeLine(
            color=ColorContinium(240, 3),
            font="./fonts/helvR12.bdf",
            fmt="%m/%d/%y",
            height=10,
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
    screen2 = Screen()
    screen2.registerElement(scrolling)
    screen2.registerElement(timeline)
    display.registerScreen(screen1)
    display.registerScreen(screen2)
    if not display.process():
        display.print_help()
