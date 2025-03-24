from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioSchemaBase, UsuarioSchemaCreate, UsuarioSchemaUpdate, CredenciaisAdmin
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
        
@router.post('/admin/signup', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaBase, include_in_schema=False)
async def post_usuario(
    usuario: UsuarioSchemaCreate, 
    credenciais: CredenciaisAdmin,
    db: AsyncSession = Depends(get_session_barra)
):
    admin_user = await get_current_admin_user(credenciais.login_admin, credenciais.senha_admin, db)

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


@router.put('/admin/usuario/{usuario_id}', response_model=UsuarioSchemaBase, status_code=status.HTTP_202_ACCEPTED, include_in_schema=False)
async def update_usuario(
    usuario_id: int,
    usuario: UsuarioSchemaUpdate,
    credenciais: CredenciaisAdmin,
    db: AsyncSession = Depends(get_session_barra)
):
    admin_user = await get_current_admin_user(credenciais.login_admin, credenciais.senha_admin, db)
    if not admin_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado. Apenas administradores podem modificar usuários.")

    try:
        result = await db.execute(select(UsuarioModel).filter(UsuarioModel.ID == usuario_id))
        usuario_up = result.scalars().one_or_none()

        if not usuario_up:
            raise HTTPException(detail='Usuário não encontrado.', status_code=status.HTTP_404_NOT_FOUND)

        if usuario.login:
            usuario_up.LOGIN = usuario.login
        if usuario.senha and usuario.senha.strip():
            usuario_up.SENHA = gerar_hash_senha(usuario.senha)
        if usuario.descricao:
            usuario_up.DESCRICAO = usuario.descricao
        if usuario.email:
            usuario_up.EMAIL = usuario.email
        if usuario.admin is not None:
            usuario_up.ADMIN = usuario.admin
        if usuario.ativo is not None:
            usuario_up.ATIVO = usuario.ativo

        await db.commit()
        await db.refresh(usuario_up)

        return UsuarioSchemaBase.model_validate(usuario_up.__dict__)

    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Erro ao atualizar usuário.")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro interno: {str(e)}")


