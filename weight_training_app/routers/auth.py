from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..controllers.auth import AuthController
from ..schemas.auth import Token, Login
from fastapi import status
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

VALID_CLIENTS = {
    "your-client-id": "your-client-secret"
}

async def validate_client(
    client_id: str,
    client_secret: str
):
    if client_id not in VALID_CLIENTS or VALID_CLIENTS[client_id] != client_secret:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid client credentials"
        )
    return True

@router.post("/token", response_model=Token)
async def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    login_data = Login(email=form_data.username, password=form_data.password)
    return await AuthController.authenticate_user(db, login_data)