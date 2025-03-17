from fastapi import FastAPI, Request
from api.v1.api import api_router
from contextlib import asynccontextmanager
from core.database import engines
import asyncio
from starlette.middleware.base import BaseHTTPMiddleware
import traceback
from core.logger import logger
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(title="Farma Conde API")

class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            error_trace = traceback.format_exc()
            logger.error(f"Erro na requisição {request.url} - {str(e)}\n{error_trace}")
            return JSONResponse(
                status_code=500,
                content={"message": "Erro interno do servidor"},
            )

app.add_middleware(LogMiddleware)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield 

    for key, engine in engines.items():
        try:
            await engine.dispose()
        except Exception as e:
            logger.error(f"Erro ao encerrar conexões da engine {key}: {e}")

    await asyncio.sleep(1)

app.router.lifespan_context = lifespan

app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", workers=6)
