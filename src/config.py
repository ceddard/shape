from pydantic import BaseSettings, ValidationError
from exceptions import MissingEnvironmentVariableError

class Settings(BaseSettings):
    PIPELINE_FILE_PATH: str
    DATA_FILE_PATH: str
    KAFKA_TOPIC: str
    KAFKA_SERVER: str

    class Config:
        env_file = ".env"

try:
    settings = Settings()
except ValidationError as e:
    for error in e.errors():
        raise MissingEnvironmentVariableError(error['loc'][0])