from databricks import sql

from core.config import settings


class DatabricksDB:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def close(self):
        self.cursor.close()
        self.connection.close()

    def get_connection(self):
        connection = sql.connect(
            server_hostname=settings.DATABRICKS_SERVER_HOSTNAME,
            http_path=settings.DATABRICKS_SERVER_HTTP_PATH,
            access_token=settings.DATABRICKS_TOKEN,
        )

        self.connection = connection
        self.cursor = connection.cursor()

    def retrieve_data(self, query):
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows
