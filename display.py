from ledmatrix import LEDMatrix


class Display(LEDMatrix):
    def __init__(self, *args, **kwargs):
        super(Display, self).__init__(*args, **kwargs)
        self.parser.add_argument(
            "-t",
            "--text",
            help="The text to scroll on the RGB LED panel",
            default="Hello world!",
        )
        self.screens = []

    def registerScreen(self, screen):
        screen.registerDisplay(self)
        self.screens.append(screen)

    def getCanvas(self):
        return self.canvas

    def run(self):
        self.canvas = self.matrix.CreateFrameCanvas()
        while True:
            for screen in self.screens:
                screen.run()
