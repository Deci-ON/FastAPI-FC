from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from core.configs import settings

engines = {
    "PROC": create_async_engine(
        settings.DB_PROC,
        pool_size=10,  
        max_overflow=1, 
        pool_recycle=900, 
        pool_timeout=60, 
        pool_pre_ping=True, 
        future=True
    ),
    "BARRA": create_async_engine(
        settings.DB_BARRA,
        pool_size=10,
        max_overflow=1,
        pool_recycle=900,
        pool_timeout=60,
        pool_pre_ping=True,
        future=True
    ),
    "SENIOR": create_async_engine(
        settings.DB_SENIOR,
        pool_size=10,
        max_overflow=1,
        pool_recycle=900,
        pool_timeout=60,
        pool_pre_ping=True,
        future=True
    ),
}

SessionLocals = {
    "PROC": sessionmaker(
        bind=engines["PROC"], expire_on_commit=False, class_=AsyncSession
    ),
    "BARRA": sessionmaker(
        bind=engines["BARRA"], expire_on_commit=False, class_=AsyncSession
    ),
    "SENIOR": sessionmaker(
        bind=engines["SENIOR"], expire_on_commit=False, class_=AsyncSession
    ),
}