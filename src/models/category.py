from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from src.connections.database import Base


class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)

    events = relationship("Event", back_populates="category")
