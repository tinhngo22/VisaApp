from fastapi import APIRouter

from fastapi import Depends, HTTPException, Request,status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.db import get_db
from typing import Annotated
from app.core.models import User

from app.core.schemas import UserCreate, UserResponse, UserUpdate


router = APIRouter()

#get user by id
@router.get(
        "/user", 
        tags=["User"], 
        response_model=UserResponse,
        status_code = status.HTTP_201_CREATED)
def get_user(user_id:int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalars().first()

    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )
    

#create user
@router.post(
        "/user", 
        tags=["User"],
        response_model = UserResponse, 
        status_code = status.HTTP_201_CREATED)
def create_user(user:UserCreate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(User).where(User.username == user.username),
    )
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    result = db.execute(
        select(User).where(User.email == user.email),
    )
    existing_email = result.scalars().first()

    if existing_email:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    
    new_user = User(
        username = user.username,
        email = user.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


#update user
def update_user(user_id:int, user:UserUpdate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(User).where(User.id == user_id)
    )
    existing_user = result.scalars().first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.username:
        existing_user.username = user.username
    if user.email:
        existing_user.email = user.email

    db.commit()
    db.refresh(existing_user)

    return existing_user