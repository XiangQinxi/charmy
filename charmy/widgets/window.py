from ..const import Backends
from .container import Container
from .windowbase import WindowBase


class Window(WindowBase, Container):
    """Window class."""

    def __init__(self, *args, **kwargs):
        WindowBase.__init__(self, *args, **kwargs)
        self.new("children", [])
        match self["drawing.framework"]:
            case Backends.SKIA:
                self.set("ui.draw_func", self.skia_draw_func)

    def skia_draw_func(self, canvas):
        """Draw function for Skia."""
        canvas.clear(self.skia.ColorWHITE)
