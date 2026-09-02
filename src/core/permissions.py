from fastapi import Depends, HTTPException, status

from src.api.deps import get_current_user
from src.models.user import User, UserRole


def require_role(*allowed_roles: str):
    #restrict a route to specific roles

    def checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action."
            )
        return current_user

    return checker


def ensure_owner_or_admin(current_user: User, owner_id: int) -> None:
    #raise 403 unless the current user owns the resource or is an admin.
    if current_user.role == UserRole.ADMIN:
        return
    if current_user.user_id != owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not own this resource."
        )
