from fastapi.templating import Jinja2Templates

from app.core.config import BASE_DIR

TEMPLATES_DIR = BASE_DIR / "app" / "templates"

templates = Jinja2Templates(
    directory=str(TEMPLATES_DIR),
)