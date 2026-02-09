from .object import CObject


class CPos(CObject):
    """CPos is a class to store position"""

    def __init__(self, x=0, y=0):
        super().__init__()
        self.new("x", x)
        self.new("y", y)
