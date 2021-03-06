from contextlib import contextmanager
from logging import getLogger, Logger
from typing import Iterator, Tuple, ClassVar

from sqlalchemy import create_engine
from sqlalchemy.orm import Session as sqlaSession, sessionmaker
from sqlalchemy.pool import StaticPool

from .base import Base


class Database:
    """ A simplified connection interface for an SQLAlchemy engine. """
    __slots__ = ["engine", "_Session"]
    _Session: sessionmaker
    logger: ClassVar[Logger] = getLogger(__name__)

    def __init__(
        self,
        /,
        conn_args: dict = None,
        *,
        dialect: str = None,
        host: str = None,
        username: str = None,
        password: str = None,
        port: int = None,
        database_name: str = None,
        extra_engine_args: dict = None,
    ) -> None:
        kwargs = locals()
        kwargs.pop("conn_args")
        kwargs = {k: v for k, v in kwargs.items() if v}
        assert kwargs or conn_args, "Specify either conn_args or one of the kwargs"
        config = conn_args or kwargs

        uri, engine_args = self._get_connection_conf(config)
        self.engine = create_engine(uri, **engine_args)
        self._Session = sessionmaker(
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
            bind=self.engine,
        )

    # noinspection PyMethodMayBeStatic
    def _get_connection_conf(self, config) -> Tuple[str, dict]:
        """
        Automatically performs optimal parametrization of the SQLAlchemy engine.\n
        If this functionality is not desired, a manual override of this function,
        can be performed using the 'override_engine' function.

        :return: Tuple containing the SQLAlchemy database uri and engine parameters
        """
        # Make sure that at least the dialect option exists
        assert config.get("dialect", False), "Database dialect selection is mandatory"
        # If host is empty and the dialect is 'sqlite', we know the user wants :memory:
        dialect, host = config.get("dialect"), config.get("host", None)
        engine_args: dict = {"pool_pre_ping": True}
        if dialect == "sqlite":
            engine_args.update({"connect_args": {"check_same_thread": False}})
            if not host:
                engine_args.update({"poolclass": StaticPool})
            uri: str = f"{dialect}:///{host if host else ':memory:'}"
        # This is the option for all other database types, such as Postgres or MySQL
        else:
            username, password, port, database = tuple(
                config.get(attr, None)
                for attr in ("username", "password", "port", "database")
            )
            if not username and not port:
                raise ValueError("Credentials and / or port missing")
            uri: str = f"{dialect}:///{username}:{password}@{host}:{port}/{database}"
        return uri, engine_args

    def override_engine(self, uri, **kwargs):
        """
        Provides an option to manually override the auto-specced engine.\n

        :param uri: Database URI
        :param kwargs: Normal kwargs as provided to the create_engine factory
        """
        self.engine = create_engine(uri, **kwargs)

    @contextmanager
    def Session(self) -> Iterator[sqlaSession]:
        """ Provides access to a scoped ORM Session """
        session: sqlaSession = self._Session()  # noqa
        try:
            yield session
            session.commit()
        except Exception as exc:  # noqa E722
            # In case there is an error during execution we rollback,
            # so no corrupted data reaches the database or fills the cache
            session.rollback()
            raise exc
        finally:
            # Always close the session after operations
            session.close()

    def create(self, base_override=None) -> None:
        """ Creates all tables in the current Base """
        base = base_override or Base
        self.logger.info(f"Constructing Database: {str(self.engine.url)}")
        for table in base.metadata.sorted_tables:
            self.logger.info(f"     {table.name}")
        base.metadata.create_all(bind=self.engine)

    def destroy(self, base_override=None) -> None:
        """ Destroys all tables in the current Base """
        base = base_override or Base
        base.metadata.drop_all(bind=self.engine)


__all__ = ["Database"]
