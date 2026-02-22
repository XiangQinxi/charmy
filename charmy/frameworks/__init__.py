from os import environ

from .ui import window_framework_map
from .drawing import drawing_framework_map
from .backend import backend_framework_map


class Frameworks:
    drawing_name = environ.get("CHARMY_DRAWING_BACKEND", "SKIA")
    drawing = drawing_framework_map[drawing_name]()
    ui_name = environ.get("CHARMY_UI_BACKEND", "GLFW")
    ui = window_framework_map[ui_name]()
    backend_name = environ.get("CHARMY_BACKEND", "OPENGL")
    backend = backend_framework_map[backend_name]()
