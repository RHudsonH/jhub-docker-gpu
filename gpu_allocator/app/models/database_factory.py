from flask import current_app
from .sqlite_database import SQLiteDatabase

def get_database_instance(db_type):
    if db_type == 'sqlite':
        oversubscribe_limit = current_app.config['OVERSUBSCRIPTION_LIMIT']
        return SQLiteDatabase(oversubscribe_limit)
    else:
        raise ValueError(f"Unsupported db_type: {db_type}")