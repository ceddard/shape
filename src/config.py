from pydantic import ValidationError
from pydantic_settings import BaseSettings
from exceptions import MissingEnvironmentVariableError


class Settings(BaseSettings):
    """
    class Settings(BaseSettings):
    for defining the environment variables required for the application.
    """

    PIPELINE_FILE_PATH: str
    DATA_FILE_PATH: str
    KAFKA_TOPIC: str
    KAFKA_SERVER: str
    APP_NAME: str
    SPARK_UI_PORT: str
    LOGS_DIR: str
    METRICS_FILE_NAME: str
    ARTIFACT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: str
    PIPELINE_FRAMEWORK: str
    TRACE_ENGINE: str

    class Config:
        env_file = ".env"


try:
    settings = Settings()
except ValidationError as e:
    for error in e.errors():
        raise MissingEnvironmentVariableError(error["loc"][0])
