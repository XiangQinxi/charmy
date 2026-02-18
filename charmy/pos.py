from .object import CharmyObject


class Pos(CharmyObject):
    """Pos is a class to store position."""

    def __init__(self, x=0, y=0):
        super().__init__()
        self.x = x
        self.y = y

    def __call__(self, x: int | float | None = None, y: int | float | None = None):
        if x:
            self.x = x
        if y:
            self.y = y

    def __str__(self):
        """Return position in string."""
        return f"Pos({self.x}, {self.y})"
