from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.core.security import hash_password, verify_password
from src.models.user import User
from src.repository.user_repository import UserRepository
from src.schemas.user import UserUpdateRequest, ChangePasswordRequest


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def get_by_the_id(self, user_id: int) -> User:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        return user

    def update_profile(self, user: User, payload: UserUpdateRequest) -> User:
        if payload.full_name is not None:
            user.full_name = payload.full_name
        return self.user_repo.update(user)

    def change_password(self, user: User, payload: ChangePasswordRequest) -> User:
        if not verify_password(payload.old_password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old password is incorrect.")
        user.password_hash = hash_password(payload.new_password)
        return self.user_repo.update(user)
