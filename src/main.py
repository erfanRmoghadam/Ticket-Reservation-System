from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from src.api.deps import get_db
from src.core.health import check_health

from src.api.auth_routes import router as auth_route
from src.api.user_routes import router as user_route
from src.api.category_routes import router as category_route
from src.api.venue_routes import router as venue_route
from src.api.seat_routes import router as seat_route
from src.api.event_routes import router as event_route
from src.api.session_routes import router as session_router
from src.api.reservation_routes import router as reservation_router

from src.core.exception_handlers import register_exception_handlers

tags_metadata = [
    { "name": "Health","description": "Application and infrastructure health checks.", },
    { "name": "Authentication","description": "User registration, login, authentication, and logout.", },
    { "name": "Users", "description": "User profile and account-related operations.", },
    { "name": "Categories", "description": "Create and manage event categories.", },
    { "name": "Venues", "description": "Create and manage venues and their information.", },
    { "name": "Seats", "description": "Manage venue seats and seat-related information.", },
    { "name": "Events", "description": "Create, browse, search, filter, and manage events.", },
    { "name": "Reservations", "description": "Create, confirm, cancel, and manage ticket reservations.", },
    { "name": "Event Sessions", "description": "Manage event sessions, schedules, and session seat availability."}
]

app = FastAPI(
    title="Ticket Reservation System", 
    summary="A backend system for managing events, sessions, seats, and ticket reservations.", 
    description=""" Ticket Reservation System is a RESTful backend application 
    built with FastAPI. The system provides APIs for: - User authentication and authorization 
    using JWT access tokens - Event, category, venue, and seat management - Event session management -
    Seat availability tracking - Ticket reservations and reservation lifecycle management -
    PostgreSQL-based data persistence - Redis caching for read-heavy operations -
    Pagination, filtering, searching, and sorting - Concurrent reservation handling using
    database row-level locking. The project is designed as a backend-focused
    portfolio project, with an emphasis on practical backend architecture and fundamentals. """,
    version="1.1.0",
    contact={ "name": "Erfan Ramezani Moghadam",
    "url": "https://github.com/erfanRmoghadam", 
    "email": "erfanramezani47@gmail.com"},
    openapi_tags=tags_metadata
)

register_exception_handlers(app)

app.include_router(auth_route)
app.include_router(user_route)
app.include_router(category_route)
app.include_router(venue_route)
app.include_router(seat_route)
app.include_router(event_route)
app.include_router(session_router)
app.include_router(reservation_router)

@app.get("/health", tags=["Health"])
def health_check(db: Session = Depends(get_db)):
    return check_health(db)