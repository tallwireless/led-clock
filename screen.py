import time


class END_SCREEN(object):
    """When an element wants to signal it's done displaying content."""

    pass


class Screen(object):
    """A screen contains the actual content"""

    def __init__(self, duration=5):
        """

        duration  seconds; default 5, 0 for indefinite
        """
        self.elements = []
        self.display = None
        self.duration = duration

    def registerElement(self, element):
        """add element to the screen to be displayed"""
        element.registerScreen(self)
        self.elements.append(element)

    def registerDisplay(self, display):
        """allow the display to register itself"""
        self.display = display

    def run(self,):
        """Actually display the content"""
        canvas = self.display.getCanvas()
        count = 0
        s = 0

        # Center the elements on the display assuming a 32 pixel high display
        for element in self.elements:
            s += element.height
        start_offset = int((32 - s) / 2) - 1
        start_time = time.mktime(time.localtime())
        while True:
            canvas.Clear()
            offset = start_offset

            # iterate through the elements have have them draw their conent
            for element in self.elements:
                offset += element.height
                rv = element.draw(canvas, offset)
                # If the element has indicated it's time to end the screen,
                # then we return to allow the display to move on to the next
                # screen
                if rv is END_SCREEN:
                    return
                # spacing between elements
                offset += 1

            time.sleep(0.03)
            count += 1

            # have we hit our time limit yet?
            now = time.mktime(time.localtime())
            if self.duration != 0 and now - start_time > self.duration:
                return

            # give the elements a chance to update themselves
            if count % 20 == 0:
                for element in self.elements:
                    element.update()

            canvas = self.display.matrix.SwapOnVSync(canvas)
