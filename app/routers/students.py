
from fastapi import APIRouter, Depends

from app.core.authorization import get_current_student
from app.models.user import User
from app.schemas.user import UserRead

router = APIRouter(
    prefix="/api/v1/students",
    tags=["Students"],
)


@router.get("/me", response_model=UserRead)
async def get_student_profile(
    current_user: User = Depends(get_current_student),
):
    return current_user
