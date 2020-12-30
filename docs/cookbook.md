# Cookbook

This section includes practical
examples of how to use some of
the utilities in this package.

### Fixing super() Resolution for type() created classes

When trying to programatically create
classes using the type() constructor,
or the types.new_class() constructor,
you may encounter the following problem when
wanting to use a parameterless `super()` call
later on:  
`TypeError: super(type, obj): obj must be an instance or subtype of type`

Here is a simple example, to reproduce the
above case with:
````python
class Something:
    def truth(self):
        return 42


class MyThing:
    def __new__(cls, *args, **kwargs):
        dunder_dict = {
            **cls.__dict__,
            "__init__": lambda *a, **kw: None
        }
        dunder_dict.pop("__new__")

        kls = type(
            cls.__name__,
            (Something,),
            dunder_dict
        )

        return kls()
    
    def truth(self):
        return super().truth() + 8


if __name__ == '__main__':
    my_thing = MyThing()
    my_thing.truth()  # TypeErrror
````

Using utilities from this package,
the above can be fixed via:
````python
from drizm_commons.utils import (
    decorate_class_object_methods,
    decorators
)


class Something:
    def truth(self):
        return 42


class MyThing:
    def __new__(cls, *args, **kwargs):
        dunder_dict = {
            **cls.__dict__,
            "__init__": lambda *a, **kw: None
        }
        dunder_dict.pop("__new__")

        kls = type(
            cls.__name__,
            (Something,),
            dunder_dict
        )
        kls = decorate_class_object_methods(
            kls,
            decorators.resolve_super_auto_resolution,
        )

        return kls()
    
    def truth(self):
        return super().truth() + 8


if __name__ == '__main__':
    my_thing = MyThing()
    my_thing.truth()  # 50
````

See the reference for both of these Methods:  

- [resolve_super_auto_resolution](utils.md#drizm_commons.utils.decorators.resolve_super_auto_resolution)  

- [decorate_class_object_methods](utils.md#drizm_commons.utils.various.decorate_class_object_methods)
