from .object import CharmyObject


class Rect(CharmyObject):
    """Rect is a class to store the position and size of a rectangle.

    Args:
        **kwargs: The keyword arguments to initialize the rectangle.
            The keyword arguments are:
                x (int): The x coordinate of the top-left corner of the rectangle.
                y (int): The y coordinate of the top-left corner of the rectangle.
                width (int): The width of the rectangle.
                height (int): The height of the rectangle.
                left (int): The left coordinate of the top-left corner of the rectangle.
                top (int): The top coordinate of the top-left corner of the rectangle.
                right (int): The right coordinate of the top-left corner of the rectangle.
                bottom (int): The bottom coordinate of the top-left corner of the rectangle.
    """

    def __init__(self, **kwargs):
        super().__init__()
        # 基础四要素
        self.base_x = 0
        self.base_y = 0
        self.base_width = 0
        self.base_height = 0

        self.__call__(**kwargs)

    def __call__(self, **kwargs):
        if "x" in kwargs:
            self.base_x = kwargs.get("x", 0)
        if "y" in kwargs:
            self.base_y = kwargs.get("y", 0)
        if "width" in kwargs:
            self.base_width = kwargs.get("width", 0)
        if "height" in kwargs:
            self.base_height = kwargs.get("height", 0)
        #############################################################
        if "left" in kwargs:
            self.base_x = kwargs.get("left", 0)
        if "top" in kwargs:
            self.base_y = kwargs.get("top", 0)
        if "right" in kwargs:
            self.base_width = kwargs.get("right", 0) - self.base_x
        if "bottom" in kwargs:
            self.base_height = kwargs.get("bottom", 0) - self.base_y

    def __str__(self):
        """Return position in string."""
        return f"Rect({self.base_x}, {self.base_y}, {self.base_width}, {self.base_height})"

    # region Attributes set/get

    @property
    def left(self):
        return self.base_x

    @left.setter
    def left(self, x):
        self.base_x = x

    @property
    def top(self):
        return self.base_y

    @top.setter
    def top(self, y):
        self.base_y = y

    @property
    def right(self):
        return self.base_x + self.base_width

    @right.setter
    def right(self, x):
        self.base_width = x - self.base_x

    @property
    def bottom(self):
        return self.base_y + self.base_height

    @bottom.setter
    def bottom(self, y):
        self.base_height = y - self.base_y

    @property
    def width(self):
        return self.base_width

    @width.setter
    def width(self, w):
        self.base_width = w

    @property
    def height(self):
        return self.base_height

    @height.setter
    def height(self, h):
        self.base_height = h

    # endregion
