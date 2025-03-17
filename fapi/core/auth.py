from pytz import timezone
from typing import Optional
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from core.configs import settings
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.usuario_model import UsuarioModel
from core.security import verificar_senha  

oauth2_schema = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login")


async def autenticar(login: str, senha: str, db: AsyncSession) -> Optional[int]:
    try:
        query = select(UsuarioModel).where(UsuarioModel.LOGIN == login, UsuarioModel.ATIVO == True)
        result = await db.execute(query)
        usuario = result.scalars().first()

        if not usuario or not verificar_senha(senha, usuario.SENHA):
            return None  

        return usuario.ID  

    except Exception as e:
        await db.rollback()  
        raise e  

    finally:
        if db.is_active:
            await db.invalidate() 
        await db.close() 



def _criar_token(tipo_token: str, tempo_vida: timedelta, sub: str) -> str:
    payload = {}
    sp = timezone("America/Sao_Paulo")
    expira = datetime.now(tz=sp) + tempo_vida

    payload["type"] = tipo_token
    payload["exp"] = expira
    payload["iat"] = datetime.now(tz=sp)
    payload["sub"] = str(sub)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

def criar_token_acesso(sub: str) -> str:
    return _criar_token(
        tipo_token="access_token",
        tempo_vida=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )
