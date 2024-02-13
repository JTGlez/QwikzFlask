import psycopg2
from psycopg2 import DatabaseError
from decouple import config

def get_conn():
    """Returns a single connection to the database.

    Raises:
        e: DatabaseError

    Returns:
        connection: Database connection to execute queries and stored procedures
    """
    try:
        conn = psycopg2.connect(
            host=config('RDS_HOSTNAME'),
            user=config('RDS_USERNAME'),
            password=config('RDS_PASSWORD'),
            database=config('DB_NAME')
        )
        return conn

    except DatabaseError as e:
        raise e
