from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session

from app.models.models import User, Role
from app.schemas.user import User as UserSchema, Role as RoleSchema, CreateUser as CreateUserSchema, Token, BaseRole
from app.api.dependencies.security import get_current_user, authenticate_user, hash_password
from app.db.session import get_db
from app.db import crud


router = APIRouter()

@router.post('/', response_model=UserSchema)
async def create_user(user: CreateUserSchema, db: Session = Depends(get_db)):
    user.password = hash_password(user.password)
    user_model = User(**user.model_dump())
    new_user = crud.save_entity(model=user_model, db=db)

    return new_user   

@router.post('/role', response_model=RoleSchema)
async def create_role(role: BaseRole, db: Session = Depends(get_db)):   
    role_model = Role(**role.model_dump())

    return crud.save_entity(model=role_model, db=db)

@router.get('/', response_model=list[UserSchema])
async def read_all_users(db: Session = Depends(get_db)) -> list[User]:
    return crud.get_all_entities(model=User, db=db)

@router.get('/me', response_model=UserSchema)
async def read_current_user(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

@router.post('/token')
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)) -> Token:
    user_access_token = authenticate_user(form_data.username, form_data.password, db=db)

    return Token(access_token=user_access_token, token_type='bearer')

@router.get('/roles', response_model=list[RoleSchema])
async def read_all_roles(db: Session = Depends(get_db)):
    return crud.get_all_entities(model=Role, db=db)

@router.delete('/')
async def delete_user(current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    return crud.delete_entity(model=User, entity_id=current_user.id, db=db)