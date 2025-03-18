from pydantic import BaseModel
from typing import Optional, List

class ProdutoSchema(BaseModel):
    produto: int
    descricao: str
    descricao_ecommerce: Optional[str]

class ProdutoResponseSchema(BaseModel):
    page: int
    total_pages: int
    total_items: int
    items_per_page: int
    produtos: List[ProdutoSchema]