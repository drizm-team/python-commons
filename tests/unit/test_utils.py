from drizm_commons.utils import (
    Path,
    _TfvarsParser,  # noqa not in __all__
    Tfvars
)


def test010_path():
    Path()


def test020_tfvars():
    path = Path(__file__).parents[1] / "data" / "testing.tfvars"
    tfvars = Tfvars(path)
    assert tfvars.vars.db_comment == "Whatever"
    assert hasattr(tfvars.vars, "empty")
    assert not tfvars.vars.empty
    assert not hasattr(tfvars.vars, "okay-whatever")
    assert tfvars.vars.okay_whatever == "hm"
    assert tfvars.vars.yes == 3.5
    assert tfvars.vars.okay == 3
