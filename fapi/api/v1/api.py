from fastapi import APIRouter
from api.v1.endpoints import produtos, usuarios, pooladmin, ping
from core.configs import settings


api_router = APIRouter()

api_router.include_router(ping.router, prefix=settings.API_V1_STR, tags=["API Status"])
api_router.include_router(produtos.router, prefix=settings.API_V1_STR, tags=["Produtos"])
api_router.include_router(usuarios.router, prefix=settings.API_V1_STR, tags=["Usuarios"])

# api_router.include_router(pooladmin.router, prefix=settings.API_V1_STR, tags=["Pool"])