from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from src.data.db import SessionDep
from src.models.user import User, UserCreate
from src.models.token import Token
from src.auth_utils import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, timedelta




router = APIRouter(prefix="/auth")



@router.post("/register", status_code=201)
async def register_user(
    session: SessionDep, 
    user_in: UserCreate
):
    """
    """
    try:
        statement = select(User).where(User.username == user_in.username)
        
        if session.exec(statement).first():
            raise HTTPException(status_code=400, detail="Username already registered")
        
        new_user = User(
            username=user_in.username,
            email=user_in.email,
            full_name=user_in.full_name,
            hashed_password=get_password_hash(user_in.password)
        )
        
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return {"message": "User created successfully"}


    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        session.rollback()
        print(f"Error during registration: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Could not save user to database"
        ) from e



@router.post("/token")
async def login_for_access_token(
    session: SessionDep,
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Token:
    """
        Searches for user in DB
    """
    try:
        statement = select(User).where(User.username == form_data.username)
        user      = session.exec(statement).first()
        
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token         = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")
    
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        print(f"Error during login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error"
        ) from e