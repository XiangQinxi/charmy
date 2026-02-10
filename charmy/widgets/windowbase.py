import importlib
import sys
import typing

from ..const import UIFrame, DrawingFrame, BackendFrame
from ..object import CObject
from ..pos import CPos
from ..size import CSize
from .app import CApp

from ..event import CEventHandler


class CWindowBase(CEventHandler):
    """CWindowBase is a base class for window

    Parameters:
        parent: The parent CApp object,
        title: The title of the window,
        size: The size of the window,
        fha: Whether to force hardware acceleration
    """

    def __init__(
        self,
        parent: CApp = None,
        *,
        title: str = "Charmy GUI",
        size: tuple[int, int] = (100, 100),
        fha: bool = True,
    ):
        super().__init__()

        # Auto find CApp Object
        if parent is None:
            parent = self.get_obj("capp0")
            if parent is None:
                raise ValueError("Not found CApp")

        # Init parent attribute
        self.new("parent", parent)

        if isinstance(parent, CApp):
            self.new("app", parent)
        elif isinstance(parent, CWindowBase):
            self.new("app", parent.get("app"))
        self.get("app").get("windows").append(self)

        # Init Attributes
        self.new(
            "ui.framework", self._get_ui_framework(), get_func=self._get_ui_framework
        )  # The UI Framework
        self.new(
            "ui.is_vsync", self._get_ui_is_vsync(), get_func=self._get_ui_is_vsync
        )  # Whether to enable VSync

        match self["ui.framework"]:
            case UIFrame.GLFW:
                self.glfw = importlib.import_module("glfw")
            case UIFrame.SDL:
                self.sdl3 = importlib.import_module("sdl3")
            case _:
                raise ValueError(f"Unknown UI Framework: {self['ui.framework']}")

        self.new("drawing.framework", self._get_drawing_framework(), get_func=self._get_drawing_framework)

        match self["drawing.framework"]:
            case DrawingFrame.SKIA:
                self.skia = importlib.import_module("skia")
            case _:
                raise ValueError(f"Unknown Drawing Framework: {self['drawing.framework']}")

        self.new("backend.framework", self._get_backend_framework(), get_func=self._get_backend_framework)

        match self["backend.framework"]:
            case BackendFrame.OPENGL:
                self.opengl = importlib.import_module("OpenGL")
            case _:
                raise ValueError(
                    f"Unknown Backend Framework: {self['backend.framework']}")

        self.new("is_force_hardware_acceleration", fha)
        self.new("pos", CPos(0, 0))  # Always (0, 0)
        self.new(
            "root_pos", CPos(0, 0), set_func=self._set_pos, get_func=self._get_pos
        )  # The position of the window
        self.new(
            "size",
            CSize(size[0], size[1]),
            set_func=self._set_size,
            get_func=self._get_size,
        )  # The size of the window
        self.new("title", title)  # The title of the window
        self.new("is_visible", False)  # Is the window visible
        self.new("is_alive", True)  # Is the window alive

        self.new("the_window", self.create())  # GLFW/SDL Window
        self.create_event_bounds()

    def create(self):
        window = None

        match self.get("ui.framework"):
            case UIFrame.GLFW:
                import glfw

                glfw.window_hint(
                    glfw.CONTEXT_RELEASE_BEHAVIOR, glfw.RELEASE_BEHAVIOR_NONE
                )  # mystery optimize
                glfw.window_hint(glfw.STENCIL_BITS, 8)
                glfw.window_hint(glfw.COCOA_RETINA_FRAMEBUFFER, glfw.TRUE)  # macOS
                glfw.window_hint(glfw.SCALE_TO_MONITOR, glfw.TRUE)  # Windows/Linux

                # see https://www.glfw.org/faq#macos
                if sys.platform.startswith("darwin"):
                    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
                    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
                    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
                    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
                else:
                    if self.get("is_force_hardware_acceleration"):
                        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
                        glfw.window_hint(glfw.CLIENT_API, glfw.OPENGL_API)
                        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
                        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
                        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

                _size = self.get("size", skip=True)
                window = glfw.create_window(
                    _size["width"], _size["height"], self.get("title"), None, None
                )
                if not window:
                    raise RuntimeError("Can't create window")

                self.set("is_visible", True)

                pos = glfw.get_window_pos(window)

                _root_point = self.get("root_pos", skip=True)
                _root_point.set("x", pos[0])
                _root_point.set("y", pos[1])

        return window

    def create_event_bounds(self):
        match self.get("ui.framework"):
            case UIFrame.GLFW:
                self.glfw.set_window_size_callback(
                    self["the_window"],
                    lambda window, width, height: self.trigger("on_resize", width=width, height=height),
                )
                self.glfw.set_window_pos_callback(
                    self["the_window"],
                    lambda window, root_x, root_y: self.trigger("on_move", x_root=root_x, y_root=root_y),
                )

    def update(self):
        pass

    def destroy(self) -> None:
        """Destroy the window.

        :return: None
        """
        # self._event_init = False
        # print(self.id)
        self["app"].destroy_window(self)
        match self.get("ui.framework"):
            case UIFrame.GLFW:
                import glfw

                try:
                    glfw.destroy_window(self["the_window"])
                except TypeError:
                    pass

        self["is_alive"] = False
        # self.draw_func = None
        self["the_window"] = None  # Clear the reference

    def can_be_close(self, value: bool | None = None) -> typing.Self | bool:
        """Set whether the window can be closed.

        Prevent users from closing the window, which can be used in conjunction with prompts like "Save before closing?"

        >>> def delete(_: SkEvent):
        >>>     window.can_be_close(False)
        >>> window.bind("delete_window", delete)


        :param value: Whether the window can be closed
        :return: None
        """
        match self.get("ui.framework"):
            case UIFrame.GLFW:
                import glfw

                if value is not None:
                    glfw.set_window_should_close(self["the_window"], value)
                    return self
                else:
                    if self["the_window"]:
                        return glfw.window_should_close(self["the_window"])
                    else:
                        return False
        return True

    # region Getters and Setters
    def _get_ui_framework(self):
        return self["app"].get("ui.framework")

    def _get_drawing_framework(self):
        return self["app"].get("drawing.framework")

    def _get_backend_framework(self):
        return self["app"].get("backend.framework")

    def _get_ui_is_vsync(self):
        return self["app"].get("ui.is_vsync")

    def _set_size(self, size: CSize | tuple[int, int]) -> None:
        if isinstance(size, tuple):
            match self["ui.framework"]:
                case UIFrame.GLFW:
                    _size = self.get("size", skip=True)
                    self.glfw.set_window_size(self["the_window"], size[0], size[1])
                    _size.set("width", size[0])
                    _size.set("height", size[1])
        else:
            match self["ui.framework"]:
                case UIFrame.GLFW:
                    self.set("size", size, skip=True)
                    self.glfw.set_window_size(
                        self["the_window"], size["width"], size["height"]
                    )
        self.trigger("on_resize")

    def _get_size(self) -> None:
        if self["ui.framework"] == UIFrame.GLFW:
            _size = self.get("size", skip=True)
            size = self.glfw.get_window_size(self["the_window"])
            _size.set("width", size[0])
            _size.set("height", size[1])

    def resize(self, size: CSize | tuple[int, int]) -> None:
        """Resize the window to the given size.

        Parameters:
            size: Size to resize
        Returns:
            None
        """
        self.set("size", size)

    def _set_pos(self, pos: CPos | tuple[int, int]) -> None:
        if isinstance(pos, tuple):
            if self["ui.framework"] == UIFrame.GLFW:
                _root_point = self.get("root_pos", skip=True)
                self.glfw.set_window_pos(self["the_window"], pos[0], pos[1])
                _root_point.set("x", pos[0])
                _root_point.set("y", pos[1])
        else:
            if self["ui.framework"] == UIFrame.GLFW:
                self.set("root_pos", pos, skip=True)
                self.glfw.set_window_pos(self["the_window"], pos["x"], pos["y"])
        self.trigger("on_move")

    def _get_pos(self) -> None:
        if self["ui.framework"] == UIFrame.GLFW:
            _root_point = self.get("root_pos", skip=True)
            pos = self.glfw.get_window_pos(self["the_window"])
            _root_point.set("x", pos[0])
            _root_point.set("y", pos[1])

    def move(self, pos: CPos | tuple[int, int]) -> None:
        """Move the window to the given position.

        Parameters:
            pos: Position to move
        Returns:
            None
        """
        self.set("root_pos", pos)

    # endregion

    # region Events

    # endregion
