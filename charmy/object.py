"""
Basic object class.
"""

import typing
import weakref

from .const import ID


class InstanceCounterMeta(type):
    """
    InstanceCounterMeta
    """

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls._instances = weakref.WeakSet()

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)

        if type(instance) is cls:
            cls._instances.add(instance)

        return instance


class CharmyObject(metaclass=InstanceCounterMeta):
    """CharmyObject is this project's basic class.

    CharmyObject provides abilities of cummulating ID and set attributes.
    """

    objects: typing.Dict[str, typing.Any] = {}  # find by ID {1: OBJ1, 2: OBJ2}
    objects_sorted: typing.Dict[str, typing.Any] = (
        {}
    )  # find by class name {OBJ1: {1: OBJECT1, 2: OBJECT2}}
    attributes: typing.Dict[str, typing.Any] = {}

    def __init__(self, id_: ID | str = ID.AUTO):
        """CharmyObject is this project's basic class.

        CharmyObject provides abilities of cumulating ID and set attributes.

        Args:
            id_ (ID | str): Optional, ID for the object
        """

        # self._attributes -> {key: value, key2: ["@custom", value, set_func, get_func]}
        # self._attributes[key] -> ["@custom", value, set_func, get_func] | value

        if id_ == ID.AUTO:
            _prefix = self.class_name
            id_ = _prefix + str(self.instance_count)
        if id_ in self.objects:
            raise KeyError(id_)
        if id_ != ID.NONE:
            self.objects[id_] = self
            self.id: typing.Final[str] = id_  # Do not change after initialization

            if self.class_name not in self.objects_sorted:
                self.objects_sorted[self.class_name] = {self.id: self}
            else:
                self.objects_sorted[self.class_name][self.id] = self

    # region: Properties

    @property
    def class_name(self) -> str:
        """Returns the class name."""
        return self.__class__.__name__

    @property
    def instances(self):
        """Returns all the class instances."""
        return self.__class__.objects_sorted[self.class_name]

    @property
    def instance_count(self):
        """Returns the class instance count."""
        return len(self._instances)
    
    # endregion

    # region: Object search

    def get_obj(self, target_id: str, default=None) -> typing.Any | None:
        """Get registered object by id. (If not found, return default)"""
        try:
            return self.__class__.objects[target_id]
        except KeyError:
            return default

    find = get_obj

    # endregion
    
    # region: Attributes set / get

    def cset(self, name: str, value: typing.Any):
        """Set shared attributes in CharmyObject.
        
        Args:
            name: Name of the attribute to set
            value: Value to set
        """
        self.attributes[name] = value

    def cget(self, name: str, default: typing.Any = None) -> typing.Any:
        """Get shared attributes in CharmyObject.
        
        Args:
            name: Name of the attribute to get
            default: Default value to return if attribute not found

        Returns:
            Value of the attribute

        """
        if name in self.attributes:
            return self.attributes[name]
        return default

    def cconfig(self, **kwargs):
        """Batch set values of multiple shared attributes in CharmyObject by giving params.
        
        Args:
             **kwargs: Any configs to add
        """
        for name in kwargs.keys():
            self.cset(name, kwargs[name])

    # endregion

    # region: __str__

    def __str__(self) -> str:
        """Happens when someone boring puts a Charmy stuff into str() or print()."""
        return str(f"CharmyObject[{self.id}]")

    # endregion