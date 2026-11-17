
from fastapi import APIRouter, Depends

from app.core.authorization import get_current_lecturer
from app.models.user import User
from app.schemas.user import UserRead

router = APIRouter(
    prefix="/api/v1/lecturers",
    tags=["Lecturers"],
)


@router.get("/me", response_model=UserRead)
async def get_lecturer_profile(
    current_user: User = Depends(get_current_lecturer),
):
    return current_user
