# ClassroomLink

A Local Network-Based Interactive Classroom
Screen-Sharing and Laboratory Device Streaming System.

## Project Overview

ClassroomLink is a locally hosted web application
that allows lecturers to share their screens,
camera feeds, and laboratory device measurements
with students over a local network.

## Technology Stack

### Backend

- Python 3.13
- FastAPI
- Uvicorn
- SQLModel
- SQLite
- aiosqlite
- Alembic
- Pydantic Settings

### Frontend

- Jinja2
- HTMX
- Tailwind CSS 4
- DaisyUI
- Iconify
- JavaScript

### Real-time Communication

- WebRTC
- FastAPI WebSockets

### Hardware Integration

- PySerial
- OpenCV
- PyVISA

### Data Visualization

- Chart.js

## Development Environment

- Windows 10/11
- Python 3.13
- pip
- Node.js
- npm
- Git
- PowerShell

Docker and cloud hosting are not required.

## Installation

### 1. Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 2. Install Python dependencies

```powershell
pip install -r requirements-dev.txt
```

### 3. Install frontend dependencies

```powershell
npm install
```

### 4. Build frontend assets

```powershell
npm run build:css
```

### 5. Start the application

```powershell
python -m uvicorn app.main:app --reload
```

## Application URLs

Homepage:
http://127.0.0.1:8000

API documentation:
http://127.0.0.1:8000/docs

Health check:
http://127.0.0.1:8000/health

## Database

Database engine: SQLite

Driver: aiosqlite

ORM: SQLModel

Migration management: Alembic

Run migrations:

```powershell
alembic upgrade head
```

## Testing

Run automated tests:

```powershell
python -m pytest -q
```

## Project Architecture

The application follows a modular monolithic architecture.

- core: application configuration and infrastructure
- models: database models
- schemas: validation and data transfer objects
- repositories: database access
- services: business logic
- routers: HTTP and WebSocket endpoints
- device_connectors: laboratory hardware integration
- templates: Jinja2 HTML templates
- static: CSS, JavaScript and images

## Development Roadmap

1. Project Initialization
2. Application Foundation
3. Authentication
4. Lecturer Dashboard
5. Student Access
6. WebRTC Screen Sharing
7. Multiple Student Streaming
8. Serial Port Management
9. UART and RS-232 Integration
10. Laboratory Data Sharing
11. Camera and Microscope Streaming
12. Local Network Deployment
13. Final Testing and Optimization

## Current Progress

- [x] Phase 1: Project Initialization
- [ ] Phase 2: Application Foundation
- [ ] Phase 3: Authentication
- [ ] Phase 4: Lecturer Dashboard
- [ ] Phase 5: Student Access
- [ ] Phase 6: WebRTC Screen Sharing
- [ ] Phase 7: Multiple Student Streaming
- [ ] Phase 8: Serial Port Management
- [ ] Phase 9: UART and RS-232 Integration
- [ ] Phase 10: Laboratory Data Sharing
- [ ] Phase 11: Camera and Microscope Streaming
- [ ] Phase 12: Local Network Deployment
- [ ] Phase 13: Final Testing and Optimization
