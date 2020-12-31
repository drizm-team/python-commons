import pytest

from drizm_commons.sqla.inspect import (
    SQLAIntrospector,
    _declBaseIntrospector,
    _declClassIntrospector,
    _tblIntrospector
)
from drizm_commons.testing.truthiness import (
    all_items_equal,
    all_nested_zipped_equal,
    all_items_present
)


@pytest.mark.usefixtures("_get_test_data")
class TestIntrospection:
    def test010_introspector_factory(self):
        args = [
            (self.declarative_class, _declClassIntrospector),
            (self.declarative_instance, _declBaseIntrospector),
            (self.table_instance, _tblIntrospector)
        ]
        for (param, expected_result) in args:
            cls = SQLAIntrospector(param)
            assert isinstance(cls, expected_result)
        with pytest.raises(TypeError):
            SQLAIntrospector(object())

    def test030_attrs(self):
        declarative_instance = SQLAIntrospector(self.declarative_instance)
        declarative_class = SQLAIntrospector(self.declarative_class)
        table_instance = SQLAIntrospector(self.table_instance)

        # test classname
        with pytest.raises(NotImplementedError):
            table_instance.classname  # noqa statement has no effect
        assert declarative_instance.classname == declarative_class.classname

        # test column_attrs
        with pytest.raises(NotImplementedError):
            table_instance.column_attrs  # noqa statement has no effect
        assert declarative_instance.column_attrs == declarative_class.column_attrs
        assert all_items_present(
            declarative_instance.column_attrs,
            ("something", "something_else")
        )
        assert "validate_name" not in declarative_instance.column_attrs

        # test the other attributes
        attrlist = ("__table__", "tablename", "columns")
        for attr in attrlist:
            d_inst = getattr(declarative_instance, attr)
            d_class = getattr(declarative_class, attr)
            t_inst = getattr(table_instance, attr)
            results = [d_inst, d_class, t_inst]
            if not attr == "columns":
                assert all_items_equal(results)
            else:
                keys = [[c.key for c in columns] for columns in results]
                assert all_nested_zipped_equal(keys)
                assert not all_items_present(
                    keys[0],
                    ("something", "something_else", "validate_name")
                )

    def test030_methods(self):
        declarative_instance = SQLAIntrospector(self.declarative_instance)
        declarative_class = SQLAIntrospector(self.declarative_class)
        table_instance = SQLAIntrospector(self.table_instance)

        method_list = ("primary_keys", "unique_keys", "foreign_keys")
        introspectors = (declarative_instance, declarative_class, table_instance)
        for method in method_list:
            results = [getattr(cls, method)() for cls in introspectors]
            assert all_nested_zipped_equal(results)
