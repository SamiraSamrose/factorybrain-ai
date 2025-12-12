from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional
from ..utils.auth import decode_access_token, TokenData, check_permission
from ..config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = decode_access_token(token)
    
    if token_data is None:
        raise credentials_exception
    
    return token_data

async def get_current_active_user(current_user: TokenData = Depends(get_current_user)) -> TokenData:
    return current_user

async def require_admin(current_user: TokenData = Depends(get_current_user)):
    if not check_permission(current_user.role, "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

async def require_supervisor(current_user: TokenData = Depends(get_current_user)):
    if not check_permission(current_user.role, "supervisor"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user
