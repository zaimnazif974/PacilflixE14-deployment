# Database Connection Manager

import psycopg2
import psycopg2.extras
import os

# Reference : https://www.psycopg.org/docs/usage.html

class DatabaseManager:
    connection = psycopg2.connect(user= "postgres.divsxpdrgvkamuvwyuhf",
                        password="pacilflix123",
                        host="aws-0-ap-southeast-1.pooler.supabase.com",
                        port="6543",
                        database="postgres")

    def get_cursor():
        print('get_cursor')
        return DatabaseManager.connection.cursor()

    def get_dict_cursor():
        return DatabaseManager.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    def commit():
        DatabaseManager.connection.commit()

    def rollback():
        DatabaseManager.connection.rollback()
    
from django.db.backends.utils import CursorWrapper


def dict_fetchall(cursor: CursorWrapper):
    """
    Return all rows from a cursor as a dict.
    Assume the column names are unique.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def dict_fetchone(cursor: CursorWrapper):
    """
    Return one row from a cursor as a dict.
    Assume the column names are unique.
    """
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    if row is None:
        return None
    return dict(zip(columns, row))
