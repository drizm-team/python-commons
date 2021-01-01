import pytest
import uuid
import datetime
import sqlalchemy as sqla
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

from drizm_commons.sqla import Database
from drizm_commons.utils.pathing import Path

TEST_ROOT = Path(__file__).parent

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    thing = None
    pk = sqla.Column(
        sqla.Integer(),
        sqla.Sequence("%(table_name)s_id_seq"),
        primary_key=True
    )
    name = sqla.Column(sqla.String)
    age = sqla.Column(sqla.Integer)
    date_of_birth = sqla.Column(sqla.Date)

    @property
    def something(self):
        return 42

    @hybrid_property
    def something_else(self):
        return 13

    @validates("name")
    def validate_name(self, _, v) -> str:
        return v


@pytest.fixture(scope="class")
def get_db():
    db = Database(dialect="sqlite")
    db.create(base_override=Base)
    yield db
    db.destroy(base_override=Base)


@pytest.fixture(scope="class")
def _get_test_data(request, get_db):
    self = request.cls
    self.declarative_class = User
    user = User(
        name="Test User",
        age=29,
        date_of_birth=datetime.date.today()
    )
    self.declarative_instance = user
    with get_db.Session() as sess:
        sess.add(user)
    with get_db.Session() as sess:
        self.table_instance = sess.query(
            self.declarative_class
        ).filter_by(pk=1).first().__table__


@pytest.fixture
def data_dump_path():
    path = TEST_ROOT / ".testdata"
    path.mkdir()

    rand_path = path / uuid.uuid4().hex
    rand_path.touch()

    yield rand_path

    path.rmdir()


__all__ = ["User", "Base"]
