from .container import CContainer
from .windowbase import CWindowBase


class CWindow(CWindowBase, CContainer):
    def __init__(self, *args, **kwargs):
        CWindowBase.__init__(self, *args, **kwargs)
        self.new("children", [])
