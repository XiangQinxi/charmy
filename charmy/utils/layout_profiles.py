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

    def _on_setattr(self, name: str, value: typing.Any) -> None:
        # super().__setattr__(name, value)
        if not name.startswith("_") and name != "type":
            self.trigger(_event.event_types.LayoutChanged(self))
            print("Layout changed")

@_dataclass
class PlaceProfile(LayoutProfile):
    """Place profile, to directly specify the position and size of the widget."""
    type: typing.ClassVar[str] = "place"

    pos: _shape.Point
    size: typing.Optional[_shape.Size] = None

class ManagedLayoutProfile(LayoutProfile):
    type: typing.ClassVar[str] = "managed"

    @property
    @_abstractmethod
    def pos(self) -> _shape.Point: ...

    @property
    @_abstractmethod
    def size(self) -> _shape.Size: ...