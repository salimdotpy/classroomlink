
from fastapi.testclient import TestClient

from app.main import app


def test_lecturer_route_requires_authentication():
    with TestClient(app) as client:
        response = client.get("/api/v1/lecturers/me")

    assert response.status_code == 401


def test_student_route_requires_authentication():
    with TestClient(app) as client:
        response = client.get("/api/v1/students/me")

    assert response.status_code == 401
