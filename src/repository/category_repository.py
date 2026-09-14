from sqlalchemy.orm import Session
from sqlalchemy import or_

from src.models.category import Category


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def search(
        self,
        search: str | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Category], int]:
        query = self.db.query(Category)

        if search:
            like = f"%{search}%"
            query = query.filter(or_(Category.name.ilike(like), Category.description.ilike(like)))

        total = query.count()
        items = query.order_by(Category.name).offset(offset).limit(limit).all()
        return items, total

    def get_category_by_id(self, category_id: int) -> Category | None:
        return self.db.query(Category).filter(Category.category_id == category_id).first()

    def create(self, category: Category) -> Category:
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def update(self, category: Category) -> Category:
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete(self, category: Category) -> None:
        self.db.delete(category)
        self.db.commit()
