import json

import pytest

from drizm_commons.sqla.encode import SqlaDeclarativeEncoder
from drizm_commons.testing.truthiness import all_keys_present


@pytest.mark.usefixtures("_get_test_data")
class TestDeclarativeEncoder:
    def test010_encode_declarative(self, data_dump_path):
        with open(data_dump_path, "w") as fout:
            json.dump(
                [self.declarative_instance],
                fout,
                indent=4,
                cls=SqlaDeclarativeEncoder
            )

        with open(data_dump_path, "r") as fin:
            content = json.load(fin)
            assert type(content) == list
            assert len(content) == 1
            assert all_keys_present(
                content[0],
                ("pk", "age", "name", "date_of_birth"),
                strict=True
            )
