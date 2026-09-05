from fastapi import FastAPI
from src.api.auth_routes import router as auth_route
from src.api.user_routes import router as user_route
from src.api.category_routes import router as category_route
from src.api.venue_routes import router as venue_route

app = FastAPI(
    title="Ticket Reservation System",
    version="1.0.0"
)

app.include_router(auth_route)
app.include_router(user_route)
app.include_router(category_route)
app.include_router(venue_route)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}