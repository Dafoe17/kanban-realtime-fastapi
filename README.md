# Kanban Realtime Board

## Overview
**A real-time collaborative Kanban board** application built with FastAPI that enables multiple users to simultaneously view and modify boards, columns, and cards with immediate synchronization across all connected clients.
Features

## 🚀 Features  
    Board Management: Create, read, update, delete boards with user access control
    Column Operations: Organize boards with columns and reorder via drag-and-drop
    Card Management: Create and manage cards within columns, assign users, move between columns
    Real-time Sync: Instant broadcasting of changes to all connected users via WebSocket
    Access Control: Role-based permissions (admin/user) with custom permission overrides
    User Authentication: JWT-based authentication with access and refresh tokens
    Invitation System: Generate shareable links for board access with expiration and usage limits
    User Preferences: Per-user board customization (colors, titles, pinning, notifications)

## 🧱 Technology Stack  
| Layer / Component | Technology / Library |
|------------------|----------------------|
| Web framework / API | FastAPI |
| ASGI server | Uvicorn |
| Database / ORM | PostgreSQL + SQLAlchemy |
| Database migrations | Alembic |
| Real-time pub/sub / cache | Redis |
| Auth / Tokens | python-jose (JWT), argon2‑cffi / passlib for password hashing |
| Data Validation / Serialization | Pydantic |
| Dev Tools / QA | ruff, black, isort, pre-commit, pytest + pytest-asyncio, httpx for testing |

## ⚙️ Installation

    Clone the repository
    git clone https://github.com/your-username/kanban-realtime-fastapi.git
    cd kanban-realtime-fastapi
    
    Install dependencies using uv:
    uv sync

    Configure environment variables (by .env.example)
    
    Set up PostgreSQL database
    
    Run database migrations:
    alembic upgrade head

    Start Redis server
    
    Run the application:
    uvicorn -m src.main:app
    or by main.py

    
## 📁 Project Structure

kanban-realtime-fastapi/  
├── src/  
│   ├── api/                      # FastAPI routers  
│   │   ├── auth.py              # Authentication endpoints  
│   │   ├── boards.py            # Board management  
│   │   ├── columns.py           # Column operations  
│   │   ├── cards.py             # Card management  
│   │   ├── invites.py           # Invitation system  
│   │   └── board_preferences.py # User preferences  
│   ├── services/                 # Business logic layer  
│   ├── repositories/             # Data access layer  
│   ├── models/                   # SQLAlchemy ORM models  
│   ├── schemas/                  # Pydantic validation schemas  
│   ├── ws/                       # WebSocket infrastructure  
│   │   ├── manager.py           # WebSocket connection manager  
│   │   ├── payloads.py          # Message schemas  
│   │   └── redis.py             # Redis pub/sub  
│   ├── core/                     # Core utilities  
│   │   └── security.py          # JWT and password functions  
│   ├── permissions.py            # Permission checking  
│   ├── database.py              # Database configuration  
│   └── redis.py                 # Redis client  
├── migrations/                   # Alembic migrations  
├── pyproject.toml               # Project configuration  
└── main.py                      # Application entry point  

## 🛠️ Architecture

The system follows a layered architecture:

    API Layer (src/api/): FastAPI routers handling HTTP requests and WebSocket connections
    Service Layer (src/services/): Business logic and permission enforcement
    Repository Layer (src/repositories/): Data access using SQLAlchemy ORM
    Real-time System (src/ws/): WebSocket connection management and Redis pub/sub

# 📘 API Reference

This section provides a complete overview of all API routers and endpoints in the Kanban Realtime FastAPI backend.

---

## 🧭 Routers Overview

| Router | Prefix | Tag | Primary Entities |
|--------|--------|------|---------------------------|
| Auth | `/auth` | 🔐 Auth | User authentication & tokens |
| Boards | `/boards` | 🗂️ Boards | Board management & membership |
| Columns | `/columns` | 📊 Columns | Column CRUD & positioning |
| Cards | `/cards` | 📄 Cards | Card CRUD, assignment & positioning |
| Invites | `/invites` | 🔗 Invites | Board invitation links |
| Preferences | `/board-preferences` | ⚙️ Preferences | User-specific board settings |

---

# 🔐 Auth API

### Endpoints

| Endpoint | Method | Purpose | Auth Required |
|----------|---------|----------|---------------------------|
| `/auth/token-json` | POST | OAuth2 token endpoint for API clients | No |
| `/auth/login` | POST | Cookie-based login for browser clients | No |
| `/auth/sign-up` | POST | User registration | No |
| `/auth/refresh` | POST | Refresh access token using refresh token | Yes (refresh token) |
| `/auth/logout` | PATCH | Invalidate tokens and clear cookies | Yes (access token) |

---

# 🗂️ Boards API

### Endpoints

| Method | Path | Operation ID | Purpose | Required Permission |
|--------|------|-----------------|-----------|-------------------------|
| GET | `/my-boards` | get-my-boards | List user's boards with pagination | Authenticated user |
| GET | `/get/{board_id}` | get-board | Retrieve specific board details | `BOARD_VIEW` |
| GET | `/get/{board_id}/users-online` | get-board-users-online | List currently connected users | `BOARD_VIEW` |
| POST | `/create` | create-board | Create a new board | Authenticated user |
| PATCH | `/patch/{board_id}` | patch-board | Update board properties | `BOARD_MANAGE` |
| PATCH | `/change-role-or-permissions/{board_id}/{user_id}` | change-role-or-permissions-board | Modify user roles or permissions | `USER_MANAGE` |
| DELETE | `/delete/{board_id}` | delete-board | Delete board and close active connections | `BOARD_MANAGE` |

---

# 📊 Columns API

### Endpoints

| Method | Endpoint | Operation ID | Response Type | Description |
|--------|-----------|------------------|----------------|-----------------------------|
| GET | `/get-board-columns/{board_id}` | get-board-columns | ColumnsListResponse | Retrieve all board columns |
| GET | `/get-column/{column_id}` | get-column | ColumnRead | Retrieve a column by ID |
| POST | `/create/in-board={board_id}` | create-column | ColumnRead | Create a new column |
| PATCH | `/patch-column/{column_id}` | patch-column | ColumnRead | Update column properties |
| PATCH | `/move-column/{column_id}` | move-column | ColumnRead | Change column position |
| DELETE | `/delete` | delete-column | ColumnRead | Delete a column and its contents |

---

# 📄 Cards API

### Endpoints

| Method | Path | Operation ID | Response Schema | Permission |
|--------|--------|----------------|--------------------|-------------------------|
| GET | `/get-column-cards/{column_id}` | get-column-cards | CardsListResponse | `BOARD_VIEW` |
| GET | `/get-card/{card_id}` | get-card | CardRead | `BOARD_VIEW` |
| PATCH | `/patch-card/{card_id}` | patch-card | CardRead | `BOARD_WRITE` |
| PATCH | `/move-card/{card_id}` | move-card | CardRead | `BOARD_WRITE` |
| POST | `/create/in-column={column_id}` | create-card | CardRead | `BOARD_WRITE` |
| DELETE | `/delete-card/{card_id}` | delete-card | CardRead | `BOARD_WRITE` |

---

# 🔗 Invites API

### Endpoints

| Method | Path | Operation ID | Response Model | Purpose |
|--------|---------------------------------|-----------------|------------------------|---------------------------|
| POST | `/invites/boards/{board_id}/invite` | create-invite | InviteRead | Create a new invite link |
| GET | `/invites/use/{invite_id}` | use-invite | UserBoardPreferencesRead | Consume invite & join board |
| GET | `/invites/info/{invite_id}` | get-invite-info | InviteRead | Retrieve invite details |
| DELETE | `/invites/delete/{invite_id}` | delete-invite | UserBoardPreferencesRead | Delete an invite |

---

# ⚙️ User Board Preferences API

### Endpoints

| Method | Path | Operation | Description |
|--------|--------|-------------|-----------------------------|
| GET | `/board-preferences/{board_id}` | get-preferences | Retrieve user preferences for a board |
| PATCH | `/board-preferences/{board_id}` | update-preferences | Update board preferences |
| DELETE | `/board-preferences/{board_id}` | reset-preferences | Reset preferences to defaults |




## 🤝 Contributing  
Contributions are welcome! Please fork the repository, create a feature branch, and submit a pull request.  
Make sure to follow formatting / linting rules (ruff, black, isort) before committing (pre-commit).  

If you want to add a new feature:  
- Add/Update API endpoints under `src/api/`  
- Implement business logic in `src/services/`  
- Add data access logic in `src/repositories/`  
- Update or create Pydantic schemas in `src/schemas/`  
- Update or create ORM models in `src/models/`  
- Add WebSocket broadcasting if the change affects real-time behavior  

