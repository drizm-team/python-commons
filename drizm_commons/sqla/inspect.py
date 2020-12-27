from abc import ABC, abstractmethod
from inspect import isclass
from typing import Union, Optional

from sqlalchemy import Table
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.exc import UnmappedClassError
from sqlalchemy.orm.util import class_mapper

from ..testing.truthiness import is_dunder


def is_mapped_class(cls) -> bool:
    """ Check whether a given class has been mapped by SQLAlchemy """
    if not isclass(cls):
        return False

    try:
        class_mapper(cls)
    except UnmappedClassError:
        return False
    else:
        return True


class _IntrospectorInterface(ABC):
    tablename: str
    columns: dict
    __table__: Table

    def __init__(self, obj) -> None:
        self.schema = obj

    @property
    @abstractmethod
    def classname(self):
        """ Name of the Declarative Base class if available """
        pass

    @property
    def column_attrs(self):
        """
        Outputs all attributes of a mapped class,
        except for properties, dunders and methods, as well as
        some of the SQLAlchemy specific attributes.

        This will include all columns that SQLAlchemy uses,
        but also attributes that the user has placed themselves.
        """
        remove_keys = (
            "metadata",  # ref to DeclarativeMeta
            "_decl_class_registry",  # declarative registry
            "_sa_class_manager"  # class state manager
        )
        attrs = [
            attr for attr in dir(
                self.schema
            ) if not is_dunder(
                attr
            ) and not callable(
                getattr(self.schema, attr)
            ) and attr not in remove_keys
        ]
        return attrs

    def primary_keys(self, retrieve_constraint: Optional[bool] = False) -> list:
        """
        Return a list of the names of all primary key columns of the model.

        :param retrieve_constraint: If this is set to true,
        the actual SQLA constraint objects will be returned as a list
        """
        constraints = inspect(self.__table__).primary_key
        if retrieve_constraint:
            return constraints

        return [c.key for c in constraints.columns]

    def unique_keys(self, include_pks: Optional[bool] = True) -> list:
        attrs_to_check = ["unique"]

        if include_pks:
            attrs_to_check.append("primary_key")

        return [
            c.name for c in self.columns if any(
                [c.primary_key, c.unique]
            )
        ]

    def foreign_keys(self, columns_only: bool = False) -> Union[list, dict]:
        foreign_keys = [c for c in self.columns if c.foreign_keys]
        fk_names = [key.name for key in foreign_keys]
        if columns_only:
            return fk_names
        fk_targets = [
            list(key.foreign_keys)[0].target_fullname for key in foreign_keys
        ]
        return {
            name: target for name, target in zip(fk_names, fk_targets)
        }


class _declBaseIntrospector(_IntrospectorInterface):
    """
    Inspect Declarative Base class instances.
    These are objects you may get back when querying,
    using a Session or when constructing an instance yourself
    """
    def __init__(self, obj) -> None:
        super().__init__(obj)
        self.tablename = obj.__tablename__
        self.columns = obj.__table__.c
        self.__table__ = obj.__table__

    @property
    def classname(self) -> str:
        return self.schema.__class__.__name__

    @property
    def column_attrs(self):
        attrs = super().column_attrs
        remove_keys = (
            "_sa_instance_state",  # instance session state manager
        )
        return [attr for attr in attrs if attr not in remove_keys]


class _declClassIntrospector(_IntrospectorInterface):
    def __init__(self, obj) -> None:
        super().__init__(obj)
        self.tablename = obj.__tablename__
        self.columns = obj.__table__.c
        self.__table__ = obj.__table__

    @property
    def classname(self) -> str:
        return self.schema.__name__


class _tblIntrospector(_IntrospectorInterface):
    def __init__(self, obj: Table) -> None:
        super().__init__(obj)
        self.tablename = obj.name
        self.columns = obj.c  # noqa false-positive write only property
        self.__table__ = obj

    @property
    def classname(self):
        raise NotImplementedError(
            f"Class {self.__class__.__name__} does not support "
            f"declarative base features"
        )

    @property
    def column_attrs(self):
        raise NotImplementedError(
            f"Autogenerated table instances do not support declarative "
            f"class properties or hybrid properties"
        )


def SQLAIntrospector(o):
    """ Factory returning a matching introspector class """
    err_msg = "Class of type {0} is not supported for introspection"
    if isinstance(o, Table):
        return _tblIntrospector(o)

    if isclass(o):
        if is_mapped_class(o):
            return _declClassIntrospector(o)
        raise TypeError(err_msg.format(type(o)))
    else:
        if is_mapped_class(o.__class__):
            return _declBaseIntrospector(o)
        raise TypeError(err_msg.format(type(o.__class__)))


__all__ = ["SQLAIntrospector", "is_mapped_class"]
