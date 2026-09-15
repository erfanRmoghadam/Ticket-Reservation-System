from sqlalchemy import text
from sqlalchemy.orm import Session

from src.connections.redis import get_redis


def check_health(db: Session) -> dict:
    checks = {"database": _check_database(db), "redis": _check_redis()}
    overall = "ok" if all(v == "ok" for v in checks.values()) else "degraded"
    return {"status": overall, "checks": checks}


def _check_database(db: Session) -> str:
    try:
        db.execute(text("SELECT 1"))
        return "ok"
    except Exception:
        return "unreachable!"


def _check_redis() -> str:
    try:
        get_redis().ping()
        return "ok"
    except Exception:
        return "unreachable!"