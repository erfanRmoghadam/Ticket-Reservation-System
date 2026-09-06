from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship

from src.connections.database import Base


class Event(Base):
    __tablename__ = "events"

    event_id = Column(Integer, primary_key=True, autoincrement=True)
    organizer_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=False)
    venue_id = Column(Integer, ForeignKey("venues.venue_id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    cover_image_url = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # sessions = relationship("EventSession", back_populates="event", cascade="all, delete-orphan")
    organizer = relationship("User", back_populates="events")
    category = relationship("Category", back_populates="events")
    venue = relationship("Venue", back_populates="events")
