from .object import CObject


class CSize(CObject):
    """CSize is a class to store size"""

    def __init__(self, width=0, height=0):
        super().__init__()
        self.new("width", width)
        self.new("height", height)
