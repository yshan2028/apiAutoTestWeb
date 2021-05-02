"""
project: apiAutoTestWeb
file: security.py
author: zy7y
date: 2021/4/17
"""
from datetime import timedelta, datetime
from typing import Optional

# token 路由
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
# jwt库
from jose import jwt, JWTError

# hash 密码库
from passlib.context import CryptContext


from db import models
from .config import setting

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 生成token 的指定路由
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_password_hash(password: str) -> str:
    """使用哈希算法加密密码"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码与hash密码"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        setting.SECRET_KEY,
        algorithm=setting.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, setting.SECRET_KEY, algorithms=[
                setting.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await models.User.get(username=username)
    if user is None:
        raise credentials_exception
    return user
