from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.api.deps import get_db
from src.core.permissions import require_role
from src.models.user import User, UserRole
from src.schemas.venue import VenueCreateRequest, VenueUpdateRequest, VenueResponse
from src.services.venue_service import VenueService

router = APIRouter(prefix="/api/venues", tags=["Venues"])


@router.get("", response_model=list[VenueResponse])
def list_venues(db: Session = Depends(get_db)):
    return VenueService(db).list_all()


@router.get("/{venue_id}", response_model=VenueResponse)
def get_venue(venue_id: int, db: Session = Depends(get_db)):
    return VenueService(db).get_by_id(venue_id)


@router.post("", response_model=VenueResponse, status_code=status.HTTP_201_CREATED)
def create_venue(
    payload: VenueCreateRequest,
    db: Session = Depends(get_db),
    _user: User = Depends(require_role(UserRole.ORGANIZER, UserRole.ADMIN)),
):
    return VenueService(db).create(payload)


@router.put("/{venue_id}", response_model=VenueResponse)
def update_venue(
    venue_id: int,
    payload: VenueUpdateRequest,
    db: Session = Depends(get_db),
    _user: User = Depends(require_role(UserRole.ORGANIZER, UserRole.ADMIN)),
):
    return VenueService(db).update(venue_id, payload)


@router.delete("/{venue_id}", status_code=204)
def delete_venue(
    venue_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_role(UserRole.ADMIN)),
):
    VenueService(db).delete(venue_id)

