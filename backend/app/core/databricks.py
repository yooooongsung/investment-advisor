from databricks import sql
from contextlib import contextmanager
from .config import settings

@contextmanager
def get_databricks_connection():
    connection = sql.connect(
        server_hostname=settings.DATABRICKS_SERVER_HOSTNAME,
        http_path=settings.DATABRICKS_HTTP_PATH,
        access_token=settings.DATABRICKS_ACCESS_TOKEN
    )
    try:
        yield connection
    finally:
        connection.close()

def execute_query(query: str, params: dict = None):
    with get_databricks_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params or {})
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.close()
        return results

def execute_update(query: str, params: dict = None):
    with get_databricks_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params or {})
        conn.commit()
        cursor.close()
