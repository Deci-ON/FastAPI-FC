from core.database import SessionLocals
import logging
from pydantic import BaseModel
from typing import AsyncGenerator, Optional
from fastapi import Depends, HTTPException, status, Request
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.auth import oauth2_schema, verificar_senha
from core.configs import settings
from models.usuario_model import UsuarioModel
    
class TokenData(BaseModel):
    username: Optional[str] = None

async def get_session_proc() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocals["PROC"]() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback() 
            raise e 
        finally:
            await safe_close(session)

async def get_session_barra() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocals["BARRA"]() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback() 
            raise e 
        finally:
            await safe_close(session)
            
async def get_session_senior() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocals["SENIOR"]() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback() 
            raise e 
        finally:
            await safe_close(session)
            
            
async def safe_close(session: AsyncSession):
    if session and session.is_active:
        await session.invalidate()
        await session.close()


async def get_current_user(request: Request, db: AsyncSession = Depends(get_session_barra), token: str = Depends(oauth2_schema)) -> UsuarioModel:    
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False}
        )
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Não foi possível autenticar a credencial",
                headers={"WWW-Authenticate": "Bearer"}
            )

        user_id = int(user_id)
        
        query = select(UsuarioModel).where(UsuarioModel.ID == user_id).limit(1)
        result = await db.execute(query)
        usuario = result.scalars().first()

        if usuario is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Não foi possível autenticar a credencial"
            )

        request.state.user = usuario  
        
        return usuario

    except (JWTError, ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erro interno ao autenticar usuário"
        )

    finally:
        if db.is_active: 
            await db.invalidate()  
        await db.close()  

        
async def get_current_admin_user(
    login: str, 
    senha: str, 
    db: AsyncSession = Depends(get_session_barra)
) -> UsuarioModel:
    try:
        query = select(UsuarioModel).filter(UsuarioModel.LOGIN == login, UsuarioModel.ATIVO == True)
        result = await db.execute(query)
        usuario = result.scalars().first()

        if not usuario or not verificar_senha(senha, usuario.SENHA):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Credenciais inválidas."
            )

        if not usuario.ADMIN:  
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado. Apenas administradores podem acessar esta funcionalidade."
            )

        return usuario
    finally:
        if db.is_active: 
            await db.invalidate()  
        await db.close()  