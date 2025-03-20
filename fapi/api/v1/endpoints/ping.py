from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/status/ping")
async def ping():
    try:
        return JSONResponse(
            content={
                "status": "pong"
                },
            )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro interno: {str(e)}")