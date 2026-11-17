
from fastapi.testclient import TestClient

from app.main import app

def test_homepage():
    """
    Verify that the homepage renders successfully.
    """

    with TestClient(app) as client:
        response = client.get("/")

        assert response.status_code == 200
        assert "ClassroomLink" in response.text
        assert "text/html" in response.headers["content-type"]

def test_health_check():
    """
    Verify application and database connectivity.
    """

    with TestClient(app) as client:
        response = client.get("/health")

        assert response.status_code == 200

        data = response.json()

        assert data["status"] == "healthy"
        assert data["application"] == "ClassroomLink"
        assert data["database"] == "connected"

def test_not_found_page():
    """
    Verify that missing browser pages return a friendly 404.
    """

    with TestClient(app) as client:
        response = client.get("/this-page-does-not-exist")

        assert response.status_code == 404
        assert "Page Not Found" in response.text or "Request Error" in response.text

def test_static_css():
    """
    Verify that compiled CSS is served locally.
    """

    with TestClient(app) as client:
        response = client.get("/static/css/output.css")

        assert response.status_code == 200
        assert len(response.content) > 0

def test_htmx_script():
    """
    Verify that HTMX is served locally.
    """

    with TestClient(app) as client:
        response = client.get("/static/js/htmx.min.js")

        assert response.status_code == 200
        assert len(response.content) > 0