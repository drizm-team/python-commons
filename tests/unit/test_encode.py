from drizm_commons.sqla.encode import SqlaDeclarativeEncoder
from tests.conftest import User
import json


def test010_encode():
    user = User(
        name="Test User",
        age=29
    )
    json.dumps(user, indent=4, cls=SqlaDeclarativeEncoder)
