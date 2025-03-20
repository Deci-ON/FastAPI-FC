from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def read_root():
    return {"message": "Bem vindo a Farma Conde API"}
