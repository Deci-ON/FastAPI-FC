from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from core.deps import get_session_proc, get_current_user
from schemas.produtos_schemas import ProdutoSchema, ProdutoResponseSchema
from models.usuario_model import UsuarioModel
from sqlalchemy.sql import text  

# Configuração do logging
logging.basicConfig(filename="database_errors.log", level=logging.ERROR,
                    format="%(asctime)s - %(levelname)s - %(message)s")

router = APIRouter()

@router.get("/produtos", response_model=ProdutoResponseSchema)
async def get_produtos(
    db: AsyncSession = Depends(get_session_proc),
    usuario: UsuarioModel = Depends(get_current_user),
    page: int = 1
):
    limit = 100
    offset = (page - 1) * limit

    query_total = text("""SELECT COUNT(*) 
        FROM PRODUTOS WITH (NOLOCK)
        WHERE 
        VENDA_CONTROLADA_INTEGRACAO = 'N'
        AND CADASTRO_ATIVO = 'S'
        AND ENVIAR_LOJAS = 'S'
        AND ENVIAR_ECOMMERCE = 'S'
    """)
    query_produtos = text("""
        SELECT produto, descricao, descricao_ecommerce
        FROM PRODUTOS WITH (NOLOCK)
        WHERE 
        VENDA_CONTROLADA_INTEGRACAO = 'N'
        AND CADASTRO_ATIVO = 'S'
        AND ENVIAR_LOJAS = 'S'
        AND ENVIAR_ECOMMERCE = 'S'
        ORDER BY PRODUTO
        OFFSET :offset ROWS FETCH NEXT :limit ROWS ONLY
    """)

    try:
        total_result = await db.execute(query_total)
        total_items = total_result.scalar() or 0
        total_pages = (total_items + limit - 1) // limit

        result = await db.execute(query_produtos, {"offset": offset, "limit": limit})
        produtos = [ProdutoSchema(**dict(zip(result.keys(), row))) for row in result.fetchall()]

        return ProdutoResponseSchema(
            page=page,
            total_pages=total_pages,
            total_items=total_items,
            items_per_page=limit,
            produtos=produtos
        )

    except Exception as e:
        logging.error(f"Erro no banco Procfit: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao buscar produtos"
        )
    finally:
        await db.close()