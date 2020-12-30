from drizm_commons.utils.tf import (
    _TfvarsParser,  # noqa not in __all__
    Tfvars
)
from drizm_commons.utils.pathing import Path
from drizm_commons.utils.type import (
    AttrDict,
    IterableKeyDictionary
)
import pytest


def test_pathing__path():
    # We basically just try and instantiate it
    # if it does not crash, which it used to do,
    # then we can consider it working
    Path()


def test_tf__tfvars():
    path = Path(__file__).parents[1] / "data" / "testing.tfvars"
    tfvars = Tfvars(path)
    assert tfvars.vars.db_comment == "Whatever"
    assert hasattr(tfvars.vars, "empty")
    assert not tfvars.vars.empty
    assert not hasattr(tfvars.vars, "okay-whatever")
    assert tfvars.vars.okay_whatever == "hm"
    assert tfvars.vars.yes == 3.5
    assert tfvars.vars.okay == 3


def test_type__attr_dict():
    obj = AttrDict({
        "test": 3,
        "something-else": "ok"
    })
    assert obj.test

    with pytest.raises(AttributeError):
        obj.something

    with pytest.raises(AttributeError):
        getattr(obj, "something")

    assert obj.something_else


def test_type__iterable_key_dict():
    obj = IterableKeyDictionary({
        3: "ok",
        ("action", "aktion"): "return",
        (5, 7): "yes"
    })

    assert obj[3]
    assert obj["action"]

    with pytest.raises(KeyError):
        obj["3"]

    assert obj[7]

    assert obj.get((5, 7))
