from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from weight_training_app.schemas.auth import TokenData
from ..database.database import get_db
from ..schemas.user import UserCreate, UserResponse, UserUpdate
from ..controllers.user import UserController
from ..utils.security import check_permissions
from ..models.user import User, UserType
from ..utils.security import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    _=Depends(check_permissions([UserType.ADMIN]))
):
    return await UserController.create_user(db, user)

@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _=Depends(check_permissions([UserType.ADMIN, UserType.TRAINER]))
):
    return await UserController.get_users(db, skip, limit)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    user_token: TokenData = Depends(get_current_user)
):
    current_user: User = await UserController.get_user_by_email(db, user_token.email)
    if (current_user.id == user_id or 
        current_user.user_type in [UserType.ADMIN, UserType.TRAINER]):
        user = await UserController.get_user_by_id(db, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    raise HTTPException(
        status_code=403,
        detail="Not authorized to access this user's data"
    )

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    user_token: TokenData = Depends(get_current_user)
):
    if user_token.user_type == UserType.ADMIN:
        return await UserController.update_user(db, user_id, user_update)
    
    current_user: User = await UserController.get_user_by_email(db, user_token.email)
    if current_user.id == user_id:
        return await UserController.update_user(db, user_id, user_update)
        
    raise HTTPException(
        status_code=403,
        detail="Not authorized to update this user's data"
    )

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _=Depends(check_permissions([UserType.ADMIN]))
):
    return await UserController.delete_user(db, user_id)