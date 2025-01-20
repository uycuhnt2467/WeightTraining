from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.auth import Login
from ..utils.security import verify_password, create_access_token
from datetime import timedelta
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class AuthController:
    @staticmethod
    async def authenticate_user(db: Session, login_data: Login) -> Dict[str, str]:
        user = db.query(User).filter(User.email == login_data.email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is disabled",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user.email, "user_type": user.user_type.value},
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}