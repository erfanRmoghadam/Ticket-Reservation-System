from sqlalchemy.orm import Session

from src.models.category import Category


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> list[Category]:
        return self.db.query(Category).order_by(Category.name).all()

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
