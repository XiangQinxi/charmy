from ..object import CObject


class CContainer(CObject):
    def __init__(self):
        super().__init__()

        self.new("children", [])
