from pydantic import BaseSettings, HttpUrl


class DataAppSettings(BaseSettings):
    url: HttpUrl = "http://0.0.0.0:8085"


class AlgoAppSettings(BaseSettings):
    url: HttpUrl = "http://0.0.0.0:8086"
