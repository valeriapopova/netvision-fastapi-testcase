from sqlalchemy import create_engine, text
from sqlalchemy.orm.session import sessionmaker


class PGDB:
    def __init__(self, **kwargs):
        """
        Parameters expected in the current implementation:

        :host: The hostname or IP address of the PostgreSQL server.
        :username: The PostgreSQL username.
        :password: The password for username.
        :database:  The database for the connection.
        :port: The PostgreSQL port.
        """
        self.db = (
            f'postgresql://{kwargs["username"]}:'
            f'{kwargs["password"]}@{kwargs["host"]}:'
            f'{kwargs["port"]}/{kwargs["database"]}'
        )
        self.engine = create_engine(self.db, echo=False)
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
