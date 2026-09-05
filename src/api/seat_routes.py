from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.api.deps import get_db
from src.core.permissions import require_role
from src.models.user import User, UserRole
from src.schemas.seat import BulkSeatCreateRequest, SeatUpdateRequest, SeatResponse
from src.services.seat_service import SeatService

router = APIRouter(prefix="/api", tags=["Seats"])


@router.post("/venues/{venue_id}/seats", response_model=list[SeatResponse], status_code=status.HTTP_201_CREATED)
def bulk_create_seats(
    venue_id: int,
    payload: BulkSeatCreateRequest,
    db: Session = Depends(get_db),
    _user: User = Depends(require_role(UserRole.ORGANIZER, UserRole.ADMIN)),
):
    return SeatService(db).bulk_create(venue_id, payload)


@router.put("/seats/{seat_id}", response_model=SeatResponse)
def update_seat(
    seat_id: int,
    payload: SeatUpdateRequest,
    db: Session = Depends(get_db),
    _user: User = Depends(require_role(UserRole.ORGANIZER, UserRole.ADMIN)),
):
    return SeatService(db).update(seat_id, payload)


@router.delete("/seats/{seat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_seat(
    seat_id: int,
    db: Session = Depends(get_db),
    _user: User = Depends(require_role(UserRole.ORGANIZER, UserRole.ADMIN)),
):
    SeatService(db).delete(seat_id)
