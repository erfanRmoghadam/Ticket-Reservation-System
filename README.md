<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=rect&color=0:0F172A,100:1E3A8A&height=140&text=%F0%9F%8E%9F%EF%B8%8F%20Ticket%20Reservation%20System&fontSize=34&fontColor=ffffff&fontAlignY=55&desc=A%20concurrency-safe%20event%20and%20venue%20booking%20API&descSize=15&descAlignY=80&descColor=cbd5e1" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/Redis-7-DC382D?style=flat-square&logo=redis&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square" />
</p>

<p align="center">A RESTful ticket reservation API for events and venues — built with FastAPI, PostgreSQL, and Redis.</p>

---

## 🧭 Table of Contents

- [Overview](#overview)
- [Highlights](#highlights)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Database Schema](#database-schema)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Run with Docker](#run-with-docker-recommended)
  - [Run Locally](#run-locally)
  - [Environment Variables](#environment-variables)
- [API Reference](#api-reference)
- [Engineering Notes](#engineering-notes)
- [Roadmap](#roadmap)
- [License](#license)

---

## 📌 Overview

This project is a backend-focused implementation of a ticket reservation platform: organizers publish events tied to a venue, each event has one or more sessions (showtimes), and users reserve specific seats for a session. It's deliberately scoped as a **learning and portfolio project** — the goal was to build something with real backend engineering substance (layered architecture, authorization, concurrency-safe booking, caching) without the operational overhead of a production system (payments, notifications, full RBAC, etc. are intentionally out of scope for now — see [Roadmap](#roadmap)).

## ✨ Highlights

- **Concurrency-safe seat booking.** Reserving a seat locks only that row (`SELECT ... FOR UPDATE`) inside a database transaction, so two users racing for the same seat can never both succeed — without needing a separate distributed lock.
- **Self-expiring reservations.** A pending reservation holds its seats for a configurable window and is lazily marked `expired` — freeing the seats back up — the next time it's read. No background worker required.
- **Layered architecture.** Routes, business logic, and data access are cleanly separated (`api` → `services` → `repository` → `models`), making each layer independently testable and easy to reason about.
- **JWT authentication with role-based access.** Three roles (`user`, `organizer`, `admin`) plus ownership checks (an organizer can only edit their own events).
- **Redis-backed seat map caching** with short-TTL invalidation on every booking action, keeping the seat map close to real-time without WebSockets.

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Framework | [FastAPI](https://fastapi.tiangolo.com/) |
| Database | PostgreSQL |
| ORM | SQLAlchemy 2.0 |
| Migrations | Alembic |
| Auth | JWT (`python-jose`) + `passlib`/`bcrypt` |
| Cache | Redis |
| Containerization | Docker & Docker Compose |
| Validation | Pydantic v2 |

## 🏗️ Architecture

```mermaid
flowchart LR
    Client -->|HTTP| API[FastAPI Routes]
    API --> Service[Service Layer]
    Service --> Repo[Repository Layer]
    Repo --> DB[(PostgreSQL)]
    Service --> Cache[(Redis)]
```

Each resource (auth, users, venues, seats, events, sessions, reservations) follows the same flow: a route handles HTTP concerns and delegates to a service, the service owns business rules and talks to one or more repositories, and repositories are the only layer that touches SQLAlchemy directly.

## 🗄️ Database Schema

```mermaid
erDiagram
    USER ||--o{ EVENT : organizes
    USER ||--o{ RESERVATION : makes
    CATEGORY ||--o{ EVENT : classifies
    VENUE ||--o{ SEAT : contains
    VENUE ||--o{ EVENT : hosts
    EVENT ||--o{ EVENT_SESSION : has
    EVENT_SESSION ||--o{ SESSION_SEAT : offers
    SEAT ||--o{ SESSION_SEAT : "priced per session"
    RESERVATION ||--o{ RESERVATION_ITEM : contains
    SESSION_SEAT ||--o{ RESERVATION_ITEM : "booked as"
```

| Table | Purpose |
|---|---|
| `users` | Accounts with a role (`user` / `organizer` / `admin`) |
| `categories` | Event categories (Music, Sports, etc.) |
| `venues` | Physical locations |
| `seats` | A venue's fixed physical seat layout |
| `events` | An organizer's event, tied to a venue and category |
| `event_sessions` | A specific date/time occurrence of an event |
| `session_seats` | A seat's price & status (`available`/`reserved`/`sold`) for one specific session |
| `reservations` | A booking attempt: status, total price, expiry |
| `reservation_items` | The individual seats belonging to a reservation |

`session_seats` is the key design decision here: the same physical seat is decoupled from any single session, so it can be priced and booked independently across multiple showtimes of the same event.

## 📁 Project Structure

```
Ticket-Reservation-System/
│
├── src/
│   ├── main.py                  # FastAPI app & router registration
│   ├── config.py                # Environment-driven settings
│   │
│   ├── api/                     # Route handlers (HTTP layer)
│   │   ├── deps.py              # get_db, get_current_user
│   │   ├── auth_routes.py
│   │   ├── user_routes.py
│   │   ├── category_routes.py
│   │   ├── venue_routes.py
│   │   ├── seat_routes.py
│   │   ├── event_routes.py
│   │   ├── session_routes.py
│   │   └── reservation_routes.py
│   │
│   ├── services/                # Business logic
│   ├── repository/              # Data access (SQLAlchemy queries)
│   ├── models/                  # SQLAlchemy ORM models
│   ├── schemas/                 # Pydantic request/response models
│   │
│   ├── core/
│   │   ├── security.py          # Password hashing, JWT
│   │   └── permissions.py       # Role & ownership checks
│   │
│   └── connections/
│       ├── database.py
│       └── redis.py
│
├── alembic/                     # Database migrations (one revision per feature)
├── dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### 🐳 Run with Docker (recommended)

```bash
git clone https://github.com/<your-username>/Ticket-Reservation-System.git
cd Ticket-Reservation-System
cp .env.example .env   # see Environment Variables below
docker compose up --build
```

The API will be available at `http://localhost:8000`, with interactive Swagger docs at **`http://localhost:8000/docs`**. Migrations run automatically on container start.

### 💻 Run Locally

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # point DATABASE_URL / REDIS_URL at local services
alembic upgrade head
uvicorn src.main:app --reload
```

Requires a running local PostgreSQL and Redis instance.

### 🔐 Environment Variables

| Variable | Description | Example |
|---|---|---|
| `DATABASE_URL` | SQLAlchemy connection string | `postgresql+psycopg2://postgres:postgres@localhost:5432/ticketdb` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |
| `SECRET_KEY` | JWT signing secret | any long random string |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime | `30` |
| `RESERVATION_HOLD_MINUTES` | How long a pending reservation holds its seats | `10` |

## 📡 API Reference

Full interactive documentation is served at `/docs` (Swagger UI) and `/redoc` once the app is running. Summary below.

#### 🔑 Authentication — `/api/auth`
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/register` | Create an account | — |
| POST | `/login` | Get a JWT access token | — |
| POST | `/logout` | Client-side token discard (stateless JWT) | ✅ |
| GET | `/me` | Get the current user | ✅ |

#### 👤 Users — `/api/users`
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/me` | Current user's profile | ✅ |
| PUT | `/me` | Update profile | ✅ |
| PATCH | `/me/password` | Change password | ✅ |
| GET | `/{id}` | Get a user by ID | Admin |

#### 🏷️ Categories — `/api/categories`
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/` | List categories | — |
| GET | `/{id}` | Get a category | — |
| POST | `/` | Create a category | Admin |
| PUT | `/{id}` | Update a category | Admin |
| DELETE | `/{id}` | Delete a category | Admin |

#### 🏛️ Venues — `/api/venues`
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/` | List venues | — |
| GET | `/{id}` | Get a venue | — |
| GET | `/{id}/seats` | Get a venue's seat layout | — |
| POST | `/` | Create a venue | Organizer/Admin |
| PUT | `/{id}` | Update a venue | Organizer/Admin |
| DELETE | `/{id}` | Delete a venue | Admin |

#### 💺 Seats — `/api`
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/venues/{venue_id}/seats` | Bulk-create a venue's seat layout | Organizer/Admin |
| PUT | `/seats/{id}` | Update a seat | Organizer/Admin |
| DELETE | `/seats/{id}` | Delete a seat | Organizer/Admin |

#### 🎫 Events — `/api/events`
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/` | Browse events (filters: `category_id`, `city`, `search`) | — |
| GET | `/{id}` | Get an event | — |
| GET | `/{id}/sessions` | List an event's sessions | — |
| POST | `/` | Create an event | Organizer/Admin |
| PUT | `/{id}` | Update an event (owner only) | ✅ |
| DELETE | `/{id}` | Delete an event (owner only) | ✅ |

#### 🕒 Event Sessions — `/api`
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/events/{event_id}/sessions` | Create a session (seeds seat pricing) | Organizer/Admin |
| GET | `/sessions/{id}` | Get a session | — |
| GET | `/sessions/{id}/seats` | Get the live seat map (cached) | — |
| PUT | `/sessions/{id}` | Update a session (owner only) | ✅ |
| DELETE | `/sessions/{id}` | Delete a session (owner only) | ✅ |

#### 📅 Reservations — `/api/reservations`
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/` | Create a reservation for one or more seats | ✅ |
| GET | `/` | List the current user's reservations | ✅ |
| GET | `/{id}` | Get a reservation (owner or admin) | ✅ |
| PATCH | `/{id}/confirm` | Confirm a pending reservation | ✅ |
| DELETE | `/{id}` | Cancel a reservation, freeing its seats | ✅ |

## 🧠 Engineering Notes

**Booking concurrency.** When a reservation is created, the target `session_seats` rows are locked with `SELECT ... FOR UPDATE` inside a single transaction before their availability is checked and updated. This guarantees that if two requests race for the same seat, one succeeds and the other receives a `409 Conflict` — with no risk of double-booking — while keeping the lock scope to just the rows involved, not the whole table.

**Reservation expiry.** Rather than running a background worker (Celery, cron) to sweep expired reservations, expiry is checked lazily: any time a reservation is read, its `expires_at` is compared against the current time, and if it has passed, the reservation is marked `expired` and its seats released in that same request. This keeps the system simpler while still being correct.

## 🗺️ Roadmap

Planned next:

- Pagination, multi-field search, and sorting on event/venue listings
- Global exception handling for consistent error responses
- A real `/health` check (DB + Redis connectivity)
- A seed script for demo data
- CI (GitHub Actions) running tests on every push

