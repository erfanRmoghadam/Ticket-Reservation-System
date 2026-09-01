from fastapi import FastAPI
from src.api.auth_routes import router as auth_route

app = FastAPI(
    title="Ticket Reservation System",
    version="1.0.0"
)

app.include_router(auth_route)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}