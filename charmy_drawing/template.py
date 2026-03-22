from abc import ABC, abstractmethod


class Drawing(ABC):
    @abstractmethod
    def surface_with_gl(self, wnd):
        pass
