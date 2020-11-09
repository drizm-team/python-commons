import pytest
from sqlalchemy.ext.hybrid import hybrid_property

from drizm_commons.sqla import Database
import sqlalchemy as sqla
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    pk = sqla.Column(
        sqla.Integer(),
        sqla.Sequence("%(table_name)s_id_seq"),
        primary_key=True
    )
    name = sqla.Column(sqla.String)
    age = sqla.Column(sqla.Integer)

    @property
    def something(self):
        return 42

    @hybrid_property
    def something_else(self):
        return 13


@pytest.fixture(scope="class")
def get_db():
    db = Database(dialect="sqlite")
    db.create(base_override=Base)
    yield db
    db.destroy(base_override=Base)


__all__ = ["User", "Base"]
