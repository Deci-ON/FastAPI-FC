from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UsuarioSchemaBase(BaseModel):
    ID: Optional[int] = None
    LOGIN: str
    DESCRICAO: str
    EMAIL: EmailStr
    ADMIN: bool = False
    ATIVO: bool = True  

    class Config:
        from_attributes  = True 
        populate_by_name = True

class UsuarioSchemaCreate(BaseModel):
    LOGIN: str = Field(alias="login")
    SENHA: str = Field(alias="senha")
    DESCRICAO: str = Field(alias="descricao")
    EMAIL: EmailStr = Field(alias="email")
    ADMIN: bool = False  
    ATIVO: bool = True   

    class Config:
        from_attributes = True
        populate_by_name = True
        
class UsuarioSchemaUpdate(BaseModel):
    login: Optional[str] = Field(default=None)
    senha: Optional[str] = Field(default=None)
    descricao: Optional[str] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    admin: Optional[bool] = Field(default=None)
    ativo: Optional[bool] = Field(default=None)

    class Config:
        from_attributes = True  
        populate_by_name = True
