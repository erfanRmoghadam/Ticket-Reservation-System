from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.core.security import hash_password, verify_password, create_access_token
from src.models.user import User
from src.repository.user_repository import UserRepository
from src.schemas.auth import RegisterRequest, LoginRequest


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def register(self, payload: RegisterRequest) -> User:
        if self.user_repo.get_by_email(payload.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists.",
            )
        user = User(
            full_name=payload.full_name,
            email=payload.email,
            password_hash=hash_password(payload.password),
        )
        return self.user_repo.create(user)

    def login(self, payload: LoginRequest) -> str:
        user = self.user_repo.get_by_email(payload.email)
        if not user or not verify_password(payload.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is disabled.")
        return create_access_token(subject=str(user.user_id), extra_claims={"role": user.role})
