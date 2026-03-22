import typing

from .object import CharmyObject


class Rect(CharmyObject):
    """Rect is a class to store the position and size of a rectangle.

    Attributes:
        x (int): The x coordinate of the top-left corner of the rectangle.
        y (int): The y coordinate of the top-left corner of the rectangle.
        width (int): The width of the rectangle.
        height (int): The height of the rectangle.
        left (int): The left coordinate of the top-left corner of the rectangle.
        top (int): The top coordinate of the top-left corner of the rectangle.
        right (int): The right coordinate of the top-left corner of the rectangle.
        bottom (int): The bottom coordinate of the top-left corner of the rectangle.
    """

    def __init__(self):
        super().__init__()
        # 基础四要素
        self.set("base_x", 0)
        self.set("base_y", 0)
        self.set("base_width", 0)
        self.set("base_height", 0)

    def make_XYWH(self, x, y, width, height) -> typing.Self:
        self.set("base_x", x)
        self.set("base_y", y)
        self.set("base_width", width)
        self.set("base_height", height)
        return self

    def make_LTRB(self, left, top, right, bottom) -> typing.Self:
        self.set("base_x", left)
        self.set("base_y", top)
        self.set("base_width", right - left)
        self.set("base_height", bottom - top)
        return self

    def __str__(self):
        """Return position in string."""
        return f"Rect({self.get('base_x')}, \
                {self.get('base_y')}, \
                {self.get('base_width')}, \
                {self.get('base_height')})"

    # region Attributes set/get

    @property
    def left(self):
        return self.get("base_x")

    @left.setter
    def left(self, value):
        self.set("base_x", value)

    @property
    def top(self):
        return self.get("base_y")

    @top.setter
    def top(self, value):
        self.set("base_y", value)

    @property
    def right(self):
        return self.get("base_x") + self.get("base_width")

    @right.setter
    def right(self, value):
        self.set("base_width", value - self.get("base_x"))

    @property
    def bottom(self):
        return self.get("base_y") + self.get("base_height")

    @bottom.setter
    def bottom(self, value):
        self.set("base_height", value - self.get("base_y"))

    @property
    def x(self):
        return self.get("base_x")

    @x.setter
    def x(self, value):
        self.set("base_x", value)

    @property
    def y(self):
        return self.get("base_y")

    @y.setter
    def y(self, value):
        self.set("base_y", value)

    @property
    def width(self):
        return self.get("base_width")

    @width.setter
    def width(self, value):
        self.set("base_width", value)

    @property
    def height(self):
        return self.get("base_height")

    @height.setter
    def height(self, value):
        self.set("base_height", value)

    # endregion
