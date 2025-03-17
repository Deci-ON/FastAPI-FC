from typing import ClassVar
from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    ODBC_DRIVER: str = "ODBC Driver 17 for SQL Server"  

    DB_PROC: str = f"mssql+aioodbc://api.fc:H1JJ!ok2Qz8I@10.112.0.126/PBS_CONDE_DADOS?driver={ODBC_DRIVER}"
    DB_BARRA: str = f"mssql+aioodbc://api.fc:H1JJ!ok2Qz8I@10.112.0.125/CONDE_BARRAMENTO?driver={ODBC_DRIVER}"
    DB_SENIOR: str = f"mssql+aioodbc://api.fc:H1JJ!ok2Qz8I@10.112.0.124/SAPIENS?driver={ODBC_DRIVER}"

    DBBaseModel: ClassVar = declarative_base()
    
    JWT_SECRET: str = 'meL2td3UAdAah_-K7ovXBXsg69yJHGYaqIzR_KEVHGE'
    """
        import secrets
        token: str = secrets.token_urlsafe(32)
        token
    """
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True

settings = Settings()
