#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User
from typing import Dict


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ save the user to the database
        """
        user = User(
            email=email,
            hashed_password=hashed_password
        )
        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, **kwargs) -> User:
        """returns the first row found in the users
        Return : First row found in the users table as filtered by kwargs
        """
        if not kwargs:
            raise InvalidRequestError

        user_keys = ['id', 'email', 'hashed_password', 'session_id',
                     'reset_token']
        for key in kwargs.keys():
            if key not in user_keys:
                raise InvalidRequestError
        find_user = self._session.query(User).filter_by(**kwargs).first()
        if find_user is None:
            raise NoResultFound
        return find_user

    def update_user(self, user_id: int, **kwargs: Dict[str, str| int]) -> None:
        if not kwargs:
            raise ValueError

        user_keys = ['id', 'email', 'hashed_password', 'session_id',
                     'reset_token']
        for key in kwargs.keys():
            if key not in user_keys:
                raise ValueError

        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            setattr(user, key, value)

        self._session.commit()
