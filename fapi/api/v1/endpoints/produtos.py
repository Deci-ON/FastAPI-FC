from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from core.deps import get_session_proc, get_current_user
from schemas.schemas import ProdutoSchema
from models.usuario_model import UsuarioModel
from sqlalchemy.sql import text  

# Configuração do logging
logging.basicConfig(filename="database_errors.log", level=logging.ERROR,
                    format="%(asctime)s - %(levelname)s - %(message)s")

router = APIRouter()

@router.get("/produtos", response_model=List[ProdutoSchema])  
async def get_produtos(
    db: AsyncSession = Depends(get_session_proc),
    usuario: UsuarioModel = Depends(get_current_user),
    page: int = 1 
):
    offset = (page - 1) * 100  
    limit = 100 

    query = text("""
        SELECT PRODUTO, DESCRICAO, DESCRICAO_ECOMMERCE
        FROM PRODUTOS WITH (NOLOCK)
        ORDER BY PRODUTO
        OFFSET :offset ROWS FETCH NEXT :limit ROWS ONLY
    """)

    try:
        result = await db.execute(query, {"offset": offset, "limit": limit}) 
        rows = result.fetchall()  

        if rows:
            colunas = result.keys() 
            produtos = [dict(zip(colunas, row)) for row in rows]  
            return produtos  

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produtos não encontrados"
        )

    except Exception as e:
        erro_msg = f"Erro no banco Procfit: {str(e)}"
        logging.error(erro_msg)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao buscar produtos"
        )
    finally:
        if db.is_active:
            await db.invalidate() 
        await db.close()  
