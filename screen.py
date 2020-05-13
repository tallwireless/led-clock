import time


class END_SCREEN(object):
    pass


class Screen(object):
    def __init__(self, count=100):
        self.elements = []
        self.display = None
        self.count = count

    def registerElement(self, element):
        element.registerScreen(self)
        self.elements.append(element)

    def registerDisplay(self, display):
        self.display = display

    def run(self,):
        canvas = self.display.getCanvas()
        count = 0
        s = 0
        for element in self.elements:
            s += element.height

        start_offset = int((32 - s) / 2) - 1
        while True:
            canvas.Clear()
            offset = start_offset
            for element in self.elements:
                offset += element.height
                rv = element.draw(canvas, offset)
                if rv is END_SCREEN:
                    return
                offset += 1
            time.sleep(0.03)
            count += 1
            if count == self.count:
                return ()
            if count % 20 == 0:
                for element in self.elements:
                    element.update()
            canvas = self.display.matrix.SwapOnVSync(canvas)
