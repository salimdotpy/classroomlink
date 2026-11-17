
from fastapi import APIRouter, Depends, Request

from app.core.config import settings
from app.core.templates import templates
from app.core.web_authorization import get_current_lecturer_page
from app.models.user import User

router = APIRouter(tags=["Lecturer Web"])


@router.get("/lecturer/dashboard", name="lecturer_dashboard")
async def lecturer_dashboard(
    request: Request,
    current_user: User = Depends(get_current_lecturer_page),
):
    return templates.TemplateResponse(
        request=request,
        name="lecturer/dashboard.html",
        context={
            "app_name": settings.app_name,
            "current_user": current_user,
        },
    )
