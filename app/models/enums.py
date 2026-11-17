
from enum import Enum


class UserRole(str, Enum):
    """
    Available ClassroomLink user roles.
    """

    LECTURER = "lecturer"
    STUDENT = "student"
