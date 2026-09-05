from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models.category import Category
from src.repository.category_repository import CategoryRepository
from src.schemas.category import CategoryCreateRequest, CategoryUpdateRequest


class CategoryService:
    def __init__(self, db: Session):
        self.repo = CategoryRepository(db)

    def list_all(self) -> list[Category]:
        return self.repo.list_all()

    def get_by_id(self, category_id: int) -> Category:
        category = self.repo.get_category_by_id(category_id)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")
        return category

    def create(self, payload: CategoryCreateRequest) -> Category:
        category = Category(name=payload.name, description=payload.description)
        return self.repo.create(category)

    def update(self, category_id: int, payload: CategoryUpdateRequest) -> Category:
        category = self.get_by_id(category_id)
        if payload.name is not None:
            category.name = payload.name
        if payload.description is not None:
            category.description = payload.description
        return self.repo.update(category)

    def delete(self, category_id: int) -> None:
        category = self.get_by_id(category_id)
        self.repo.delete(category)
