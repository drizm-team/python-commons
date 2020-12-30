from drizm_commons.testing.truthiness import (
    all_keys_present,
    is_instance_method,
    is_static_method,
    is_class_method
)
import pytest


class _TestClass:
    @staticmethod
    def static_method():
        return True

    @classmethod
    def class_method(cls):
        return True

    # noinspection PyMethodMayBeStatic
    def instance_method(self):
        return True


def test__all_keys_present():
    assert all_keys_present(
        {"okay": 2}, ("okay",)
    )
    assert all_keys_present(
        {"okay": 2, "random": "bruh"}, ("okay",)
    )
    assert all_keys_present(
        {"okay": 2, "random": "bruh"}, ("random", "okay")
    )

    assert not all_keys_present(
        {"okay": 2, "random": "bruh"}, ("okay",), strict=True
    )


def test__is_methodtype():
    assert is_instance_method(_TestClass, "instance_method")
    assert is_instance_method(_TestClass(), "instance_method")
    assert not is_instance_method(_TestClass(), "class_method")
    assert not is_instance_method(_TestClass(), "static_method")

    assert is_class_method(_TestClass, "class_method")
    assert is_class_method(_TestClass(), "class_method")
    assert not is_class_method(_TestClass, "instance_method")
    assert not is_class_method(_TestClass(), "instance_method")
    assert not is_class_method(_TestClass, "static_method")
    assert not is_class_method(_TestClass(), "static_method")

    assert is_static_method(_TestClass(), "static_method")
    assert not is_static_method(_TestClass(), "class_method")
    assert not is_static_method(_TestClass(), "instance_method")
