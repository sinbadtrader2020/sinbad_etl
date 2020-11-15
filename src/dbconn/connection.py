from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from src.utils import logger


class Connection:
    def __init__(self):
        self.pool = None

        self.db_name = None
        self.db_username = None
        self.db_password = None
        self.db_hostname = None
        self.db_port = None

    def config_database(self, config):
        section_name = "DATABASE"

        self.db_name = config.get(section_name, 'DB_NAME')
        self.db_username = config.get(section_name, 'DB_USERNAME')
        self.db_password = config.get(section_name, 'DB_PASSWORD')
        self.db_hostname = config.get(section_name, 'DB_HOSTNAME')
        self.db_port = config.get(section_name, 'DB_PORT')

        logger.info('DATABASE --> ' +
                    '\n\t' + self.db_name +
                    '\n\t' + self.db_username +
                    '\n\t' + "<hidden>" +
                    '\n\t' + self.db_hostname +
                    '\n\t' + self.db_port)

        self.pool = None    # Reinitialize

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


connection = Connection()
