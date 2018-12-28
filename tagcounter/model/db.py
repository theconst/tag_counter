import functools
from typing import Callable, TypeVar

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

import resources
from model.entities import Base

T = TypeVar('T')


class DataAccessLayer:
    engine = None
    Session = None
    DEFAULT_CONNECTION_STRING = "sqlite:///{}".format(resources.DATABASE_PATH)

    def db_init(self, connection_string: str = DEFAULT_CONNECTION_STRING) -> None:
        self.engine = create_engine(connection_string)
        Base.metadata.create_all(self.engine)

        self.Session = scoped_session(sessionmaker())
        self.Session.configure(bind=self.engine)

    def transactional(self, func: Callable[..., T]) -> Callable[..., T]:
        """Transactional decorator for a function that closes the session in the scope of a single transaction"""

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            s = self.Session()
            try:
                r = func(*args, **kwargs, session=s)
                s.commit()
                return r
            except:
                s.rollback()
                raise
            finally:
                s.close()

        return wrapper


dal = DataAccessLayer()
