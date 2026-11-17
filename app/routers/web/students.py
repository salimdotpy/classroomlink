
from fastapi import APIRouter, Depends, Request

from app.core.config import settings
from app.core.templates import templates
from app.core.web_authorization import get_current_student_page
from app.models.user import User

router = APIRouter(tags=["Student Web"])


@router.get("/student/dashboard", name="student_dashboard")
async def student_dashboard(
    request: Request,
    current_user: User = Depends(get_current_student_page),
):
    return templates.TemplateResponse(
        request=request,
        name="student/dashboard.html",
        context={
            "app_name": settings.app_name,
            "current_user": current_user,
        },
    )
