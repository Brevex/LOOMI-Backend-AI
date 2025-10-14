from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import user as user_schema
from app.crud import crud_user
from app.api.v1 import deps

router = APIRouter()


@router.post("/", response_model=user_schema.User, status_code=status.HTTP_201_CREATED)
def create_user(*, db: Session = Depends(deps.get_db), user_in: user_schema.UserCreate):
    """
    Cria um novo usuário no sistema.
    """
    user = crud_user.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um usuário com este e-mail.",
        )

    user = crud_user.create_user(db=db, user=user_in)
    return user
