from starlette.config import Config

config = Config()

class Settings:
    POSTGRES_HOST = config("POSTGRES_HOST", cast=str, default=None)
    POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default=None)
    POSTGRES_DB = config("POSTGRES_DB", cast=str, default=None)
    POSTGRES_USER = config("POSTGRES_USER", cast=str, default=None)
    POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=str, default=None)

    DATABRICKS_SERVER_HOSTNAME = config("DATABRICKS_SERVER_HOSTNAME", cast=str, default=None)
    DATABRICKS_HTTP_PATH = config("DATABRICKS_HTTP_PATH", cast=str, default=None)
    DATABRICKS_TOKEN = config("DATABRICKS_TOKEN", cast=str, default=None)


settings = Settings()