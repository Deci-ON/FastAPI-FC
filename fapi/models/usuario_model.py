from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from core.configs import settings

class UsuarioModel(settings.DBBaseModel):
    __tablename__ = 'TB_USERS_FAPI'
    
    ID= Column(Integer, primary_key=True, autoincrement=True)
    LOGIN = Column(String(256), index=True, nullable=False, unique=True)
    SENHA = Column(String(256), nullable=False)
    DESCRICAO = Column(String(256), nullable=False)
    DATA_CRIACAO = Column(DateTime, default=func.now()) 
    EMAIL= Column(String(256), nullable=False)
    ADMIN = Column(Boolean, default= False)
    ATIVO = Column(Boolean, default= True)