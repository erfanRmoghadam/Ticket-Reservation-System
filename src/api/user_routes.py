from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.deps import get_current_user, get_db
from src.core.permissions import require_role
from src.models.user import User, UserRole
from src.schemas.user import UserResponse, UserUpdateRequest, ChangePasswordRequest
from src.services.user_service import UserService

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserResponse)
def update_my_profile(payload: UserUpdateRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return UserService(db).update_profile(current_user, payload)


@router.patch("/me/password", response_model=UserResponse)
def change_my_password(payload: ChangePasswordRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return UserService(db).change_password(current_user, payload)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), _admin: User = Depends(require_role(UserRole.ADMIN))):
    return UserService(db).get_by_the_id(user_id)
