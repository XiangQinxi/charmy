import typing

from ..object import CharmyObject
from .container import Container, auto_find_parent


@auto_find_parent
class Widget(CharmyObject):
    def __init__(self, parent: Container | None = None):
        super().__init__()

        self.new("parent", parent)

        # 如果有父容器，添加到子部件列表
        if parent is not None:
            parent.add_child(self)
