import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select

from datetime import datetime, timedelta, timezone
from typing import Annotated

from src.data.db import SessionDep
from src.models.user import User
from src.models.token import TokenData
from src.config import settings



AUTH_KEY   = settings.auth_key
ALGORITHM  = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes



password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")




def verify_password(plain_password, hashed_password) -> bool:
    return password_hash.verify(plain_password, hashed_password)



def get_password_hash(password) -> str:
    return password_hash.hash(password)



def create_access_token(
    data:          dict, 
    expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()

    if expires_delta is not None:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, AUTH_KEY, algorithm=ALGORITHM)
    return encoded_jwt



async def get_current_user(
    session: SessionDep,
    token:   Annotated[str, Depends(oauth2_scheme)]
) -> User:
    """
    Validate JWT token and retrieves user from Database

    Args:
        session: Database session
        token: bearer token

    Returns:
        User: authenticated user object
    """
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail      = "Couldn't validate credentials",
        headers     = {"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, AUTH_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
    
    except InvalidTokenError as exc:
        raise credentials_exception from exc
    
    user = session.exec(select(User).where(User.username == username)).first()
    
    if user is None:
        raise credentials_exception
    
    return user