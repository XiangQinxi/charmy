from __future__ import annotations as _

import typing

from dataclasses import dataclass as _dataclass
from abc import abstractmethod as _abstractmethod

from .. import event as _event
from .on_setattr import apply_on_setattr as _apply_on_setattr

if typing.TYPE_CHECKING:
    from ..styles import shape as _shape


@_apply_on_setattr
class LayoutProfile(_event.EventHandling):
    """Base class of all layout profiles."""
    type: typing.ClassVar[str] = "nolayout"

    def __init__(self):
        self._alive: bool = False

        super().__init__()

        self.pos: _shape.Point
        self.size: _shape.Size

    def _on_setattr(self, name: str, value: typing.Any, old: typing.Any) -> None:
        # super().__setattr__(name, value)
        if not hasattr(self, "_alive"):
            return
        if not self._alive:
            return
        if name != "type":
            self.trigger(_event.event_types.LayoutChanged(self, name, old))
            # print(f"Layout changed: {name}")

@_dataclass
class PlaceProfile(LayoutProfile):
    """Place profile, to directly specify the position and size of the widget."""
    type: typing.ClassVar[str] = "place"

    def __post_init__(self) -> ...:
        super().__init__()

    pos: _shape.Point
    size: typing.Optional[_shape.Size] = None

class ManagedLayoutProfile(LayoutProfile):
    type: typing.ClassVar[str] = "managed"

    @property
    @_abstractmethod
    def pos(self) -> _shape.Point: ...

    @pos.setter
    def pos(self) -> None: raise NotImplementedError(
        "Not supported to set pos for managed layout.")

    @property
    @_abstractmethod
    def size(self) -> _shape.Size: ...

    @size.setter
    def size(self) -> None: raise NotImplementedError(
        "Not supported to set size for managed layout.")