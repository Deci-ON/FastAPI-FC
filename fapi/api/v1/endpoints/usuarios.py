from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioSchemaBase, UsuarioSchemaCreate, UsuarioSchemaUpdate
from core.deps import get_session_barra, get_current_admin_user
from core.security import gerar_hash_senha
from core.auth import autenticar, criar_token_acesso

router = APIRouter()

@router.post('/login')
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_session_barra)
):
    try:
        usuario_id = await autenticar(login=form_data.username, senha=form_data.password, db=db)

        if not usuario_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Dados de acesso incorretos."
            )

        return JSONResponse(
            content={
                "access_token": criar_token_acesso(sub=usuario_id),
                "token_type": "bearer"
            },
            status_code=status.HTTP_200_OK
        )
    finally:
        await db.close() 
        
@router.post('/admin/signup', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaBase)
async def post_usuario(
    usuario: UsuarioSchemaCreate, 
    login_admin: str, 
    senha_admin: str, 
    db: AsyncSession = Depends(get_session_barra)
):
    admin_user = await get_current_admin_user(login_admin, senha_admin, db)

    if not admin_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado. Apenas administradores podem criar usuários.")

    novo_usuario = UsuarioModel(
        LOGIN=usuario.LOGIN,
        SENHA=gerar_hash_senha(usuario.SENHA),
        DESCRICAO=usuario.DESCRICAO,
        EMAIL=usuario.EMAIL,
        ADMIN=usuario.ADMIN,
        ATIVO=usuario.ATIVO
    )

    try:
        db.add(novo_usuario)
        await db.commit()  
        await db.refresh(novo_usuario)

        return UsuarioSchemaBase.model_validate(novo_usuario.__dict__) 

    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Já existe um usuário com este email.")

@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaBase)
async def post_usuario(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session_barra)):
    novo_usuario = UsuarioModel(
        LOGIN=usuario.LOGIN,
        SENHA=gerar_hash_senha(usuario.SENHA),
        DESCRICAO=usuario.DESCRICAO,
        EMAIL=usuario.EMAIL,
        ADMIN=usuario.ADMIN,
        ATIVO=usuario.ATIVO
    )

    try:
        db.add(novo_usuario)
        await db.commit()  
        await db.refresh(novo_usuario)

        return UsuarioSchemaBase.model_validate(novo_usuario.__dict__) 

    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Já existe um usuário com este email.")

@router.put('/admin/usuario/{usuario_id}', response_model=UsuarioSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def update_usuario(usuario_id: int, usuario: UsuarioSchemaUpdate,
    login_admin: str, 
    senha_admin: str,  
    db: AsyncSession = Depends(get_session_barra)):
    
    admin_user = await get_current_admin_user(login_admin, senha_admin, db)
    if not admin_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado. Apenas administradores podem criar usuários.")
    try:
        async with db.begin():
            result = await db.execute(select(UsuarioModel).filter(UsuarioModel.ID == usuario_id))
            usuario_up = result.scalars().unique().one_or_none()

            if not usuario_up:
                raise HTTPException(detail='Usuário não encontrado.', status_code=status.HTTP_404_NOT_FOUND)

            if usuario.LOGIN:
                usuario_up.LOGIN = usuario.LOGIN
            if usuario.SENHA:
                usuario_up.SENHA = gerar_hash_senha(usuario.SENHA)
            if usuario.DESCRICAO:
                usuario_up.DESCRICAO = usuario.DESCRICAO
            if usuario.EMAIL:
                usuario_up.EMAIL = usuario.EMAIL
            if usuario.ADMIN is not None:
                usuario_up.ADMIN = usuario.ADMIN
            if usuario.ATIVO is not None:
                usuario_up.ATIVO = usuario.ATIVO

            await db.commit()
            await db.refresh(usuario_up)

            return UsuarioSchemaBase.model_validate(usuario_up.__dict__)

    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Erro ao atualizar usuário.")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro interno: {str(e)}")