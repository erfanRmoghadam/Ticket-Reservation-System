from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.api.deps import get_db, get_current_user
from src.core.permissions import require_role
from src.models.user import User, UserRole
from src.schemas.session import SessionCreateRequest, SessionUpdateRequest, SessionResponse, SessionSeatResponse
from src.services.session_service import SessionService

router = APIRouter(prefix="/api", tags=["Event Sessions"])


@router.post("/events/{event_id}/sessions", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(
    event_id: int,
    payload: SessionCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ORGANIZER, UserRole.ADMIN)),
):
    return SessionService(db).create(event_id, current_user, payload)


@router.get("/sessions/{session_id}", response_model=SessionResponse)
def get_session(session_id: int, db: Session = Depends(get_db)):
    return SessionService(db).get_by_id(session_id)


@router.put("/sessions/{session_id}", response_model=SessionResponse)
def update_session(
    session_id: int,
    payload: SessionUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return SessionService(db).update(session_id, current_user, payload)


@router.delete("/sessions/{session_id}", status_code=204)
def delete_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    SessionService(db).delete(session_id, current_user)

