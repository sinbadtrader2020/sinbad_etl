from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager


class Connection:
    def __init__(self,
                 db_name=None,
                 db_username=None,
                 db_password=None,
                 db_hostname=None,
                 db_port=None):
        self.db_name = db_name
        self.db_username = db_username
        self.db_password = db_password
        self.db_hostname = db_hostname
        self.db_port = db_port

        self.pool = None

    @contextmanager
    def get_db_connection(self):
        if self.pool is None:
            self.pool = ThreadedConnectionPool(1, 20,
                                               database=self.db_name,
                                               user=self.db_username,
                                               password=self.db_password,
                                               host=self.db_hostname,
                                               port=self.db_port)

        db_connection = None
        try:
            db_connection = self.pool.getconn()
            yield db_connection
        finally:
            self.pool.putconn(db_connection)

    @contextmanager
    def get_db_cursor(self, commit=False):
        with self.get_db_connection() as connection:
            cursor = connection.cursor(
                cursor_factory=RealDictCursor)
            try:
                yield cursor
                if commit:
                    connection.commit()
            finally:
                cursor.close()


db_config = {
    'db_name': 'sinbad',
    'db_username': 'sinbad',
    'db_password': 'sinbad@finance',
    'db_hostname': 'localhost',
    'db_port': 5432
}
connection = Connection(**db_config)
