"""
Populates the database with realistic example data.

Usage:
    python -m scripts.seed
    # inside the container: docker compose exec api python -m scripts.seed

Safe to re-run: checks for existing records by email/name before creating duplicates.
"""
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from src.connections.database import SessionLocal, Base, engine
from src.core.security import hash_password
from src.models.user import User, UserRole
from src.models.category import Category
from src.models.venue import Venue
from src.models.seat import Seat
from src.models.event import Event
from src.models.event_session import EventSession
from src.models.session_seat import SessionSeat


def get_or_create(db, model, defaults=None, **lookup):
    instance = db.query(model).filter_by(**lookup).first()
    if instance:
        return instance, False
    params = {**lookup, **(defaults or {})}
    instance = model(**params)
    db.add(instance)
    db.flush()
    return instance, True


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        admin, _ = get_or_create(
            db, User, email="admin@example.com",
            defaults={"full_name": "example Admin", "password_hash": hash_password("admin123"), "role": UserRole.ADMIN},
        )
        organizer, _ = get_or_create(
            db, User, email="organizer@example.com",
            defaults={"full_name": "example Organizer", "password_hash": hash_password("organizer123"), "role": UserRole.ORGANIZER},
        )
        buyer, _ = get_or_create(
            db, User, email="buyer@example.com",
            defaults={"full_name": "example Buyer", "password_hash": hash_password("buyer123"), "role": UserRole.USER},
        )

        categories = {}
        for name, desc in [
            ("Music", "Concerts and live music performances"),
            ("Theater", "Plays and stage performances"),
            ("Sports", "Live sporting events"),
        ]:
            cat, _ = get_or_create(db, Category, name=name, defaults={"description": desc})
            categories[name] = cat

        venue, created = get_or_create(
            db, Venue, name="Baku Crystal Hall",
            defaults={"address": "1 Heydar Aliyev Ave", "city": "Baku", "total_capacity": 24},
        )

        if created:
            seats = []
            for row in ["A", "B", "C"]:
                for num in range(1, 9):
                    seat_type = "vip" if row == "A" else "normal"
                    seats.append(Seat(venue_id=venue.venue_id, row_label=row, seat_number=num, seat_type=seat_type))
            db.add_all(seats)
            db.flush()

        event, created = get_or_create(
            db, Event, title="Baku Jazz Night",
            defaults={
                "organizer_id": organizer.user_id,
                "category_id": categories["Music"].category_id,
                "venue_id": venue.venue_id,
                "description": "An evening of live jazz featuring local and international artists.",
                "cover_image_url": None,
            },
        )

        if created:
            venue_seats = db.query(Seat).filter(Seat.venue_id == venue.venue_id).all()
            start_time = datetime.now(timezone.utc) + timedelta(days=14)
            session = EventSession(event_id=event.event_id, start_time=start_time, end_time=start_time + timedelta(hours=2))
            db.add(session)
            db.flush()

            session_seats = [
                SessionSeat(
                    session_id=session.session_id,
                    seat_id=seat.seat_id,
                    price=Decimal("75.00") if seat.seat_type == "vip" else Decimal("35.00"),
                )
                for seat in venue_seats
            ]
            db.add_all(session_seats)

        db.commit()
        print("Seed complete. example accounts:")
        print("  admin@example.com     / admin123")
        print("  organizer@example.com / organizer123")
        print("  buyer@example.com     / buyer123")
    finally:
        db.close()


if __name__ == "__main__":
    seed()