import os
from typing import ClassVar
from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    ODBC_DRIVER: str = "ODBC Driver 18 for SQL Server"

    DB_USER: str = os.getenv('DB_USER')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD')
    DB_HOST_PROC: str = os.getenv('DB_HOST_PROC')
    DB_HOST_BARRA: str = os.getenv('DB_HOST_BARRA')
    DB_HOST_SENIOR: str = os.getenv('DB_HOST_SENIOR')
    DB_NAME_PROC: str = os.getenv('DB_NAME_PROC')
    DB_NAME_BARRA: str = os.getenv('DB_NAME_BARRA')
    DB_NAME_SENIOR: str = os.getenv('DB_NAME_SENIOR')

    JWT_SECRET: str = os.getenv('JWT_SECRET')
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    DB_PROC: str = f"mssql+aioodbc://{DB_USER}:{DB_PASSWORD}@{DB_HOST_PROC}/{DB_NAME_PROC}?driver={ODBC_DRIVER}&TrustServerCertificate=yes"
    DB_BARRA: str = f"mssql+aioodbc://{DB_USER}:{DB_PASSWORD}@{DB_HOST_BARRA}/{DB_NAME_BARRA}?driver={ODBC_DRIVER}&TrustServerCertificate=yes"
    DB_SENIOR: str = f"mssql+aioodbc://{DB_USER}:{DB_PASSWORD}@{DB_HOST_SENIOR}/{DB_NAME_SENIOR}?driver={ODBC_DRIVER}&TrustServerCertificate=yes"

    DBBaseModel: ClassVar = declarative_base()

    class Config:
        case_sensitive = True

settings = Settings()
