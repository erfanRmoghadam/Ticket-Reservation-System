from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from src.api.deps import get_db
from src.core.permissions import require_role
from src.models.user import User, UserRole
from src.schemas.category import CategoryCreateRequest, CategoryUpdateRequest, CategoryResponse
from src.schemas.pagination import Page
from src.services.category_service import CategoryService

router = APIRouter(prefix="/api/categories", tags=["Categories"])


@router.get("", response_model=Page[CategoryResponse])
def list_categories(
    search: str | None = Query(default=None, description="Matches against name or description"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return CategoryService(db).search(search=search, page=page, page_size=page_size)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    return CategoryService(db).get_by_id(category_id)


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreateRequest,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_role(UserRole.ADMIN)),
):
    return CategoryService(db).create(payload)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    payload: CategoryUpdateRequest,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_role(UserRole.ADMIN)),
):
    return CategoryService(db).update(category_id, payload)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_role(UserRole.ADMIN)),
):
    CategoryService(db).delete(category_id)
