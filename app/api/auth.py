from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies import SessionDep, UserDep, TokenDep
from app.schemas import Token
from app.schemas import UserCredentials
from app.core import create_access_token
from app.crud import aunthenticate


router = APIRouter()


@router.post("/token_json", response_model=Token)
async def login_for_access_token_json(
    db: SessionDep,
    data: UserCredentials,
) -> Token:
    user = aunthenticate(db, data)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect login or password")
    return Token(
        access_token=create_access_token(user.id),
    )


@router.post("/token", response_model=Token)
async def login_for_access_token(
    db: SessionDep,
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    user = aunthenticate(
        db,
        UserCredentials(login=form_data.username, password=form_data.password),
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect login or password")
    return Token(
        access_token=create_access_token(user.id),
    )

