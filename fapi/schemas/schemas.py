from pydantic import BaseModel
from typing import Optional

class ProdutoSchema(BaseModel):
    PRODUTO: int
    DESCRICAO: str
    DESCRICAO_ECOMMERCE: Optional[str]
