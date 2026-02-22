import importlib.util
from abc import ABC, abstractmethod


# region Backend
class BackendFramework(ABC):
    pass


backend_framework_map = {}


class OPENGL(BackendFramework):
    def __init__(self):
        self.opengl = importlib.import_module("OpenGL")
        self.opengl_GL = importlib.import_module("OpenGL.GL")


if importlib.util.find_spec("OpenGL") is not None:
    backend_framework_map["OPENGL"] = OPENGL  # NOQA

# endregion
