from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Literal

from src.api.deps import get_db, get_current_user
from src.core.permissions import require_role
from src.models.user import User, UserRole
from src.schemas.event import EventCreateRequest, EventUpdateRequest, EventResponse
from src.schemas.pagination import Page
from src.services.event_service import EventService


router = APIRouter(prefix="/api/events", tags=["Events"])


@router.get("", response_model=Page[EventResponse])
def list_events(
    category_id: int | None = Query(default=None),
    city: str | None = Query(default=None, description="Filter by venue city"),
    search: str | None = Query(default=None, description="Matches against title or description"),
    sort_by: Literal["created_at", "title"] = Query(default="created_at"),
    order: Literal["asc", "desc"] = Query(default="desc"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return EventService(db).search(
        category_id=category_id,
        city=city,
        search=search,
        sort_by=sort_by,
        order=order,
        page=page,
        page_size=page_size,
    )


@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    return EventService(db).get_by_id(event_id)


@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(
    payload: EventCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ORGANIZER, UserRole.ADMIN)),
):
    return EventService(db).create(current_user, payload)


@router.put("/{event_id}", response_model=EventResponse)
def update_event(
    event_id: int,
    payload: EventUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return EventService(db).update(event_id, current_user, payload)


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    EventService(db).delete(event_id, current_user)

