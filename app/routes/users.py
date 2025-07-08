from typing import Annotated, DIct

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.config import settings


users_route = APIRouter(prefix="/users")


async def get_user_id(
    token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="/users/token/"))],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> str:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        
        return user_id

    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


