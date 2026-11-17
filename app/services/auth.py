
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.enums import UserRole
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserRegister


class EmailAlreadyRegisteredError(Exception):
    """Raised when an email address is already registered."""


class AuthService:
    """
    Authentication-related business operations.
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.users = UserRepository(session)

    async def register_lecturer(self, data: UserRegister) -> User:
        """
        Register a new lecturer account.

        Passwords are hashed before persistence.
        """

        email = str(data.email).strip().lower()

        # Check for an existing account.
        existing_user = await self.users.get_by_email(email)

        if existing_user is not None:
            raise EmailAlreadyRegisteredError(
                "An account with this email already exists."
            )

        user = User(
            email=email,
            password_hash=hash_password(data.password),
            role=UserRole.LECTURER,
            is_active=True,
        )

        try:
            await self.users.create(user)

            await self.session.commit()

            await self.session.refresh(user)

        except IntegrityError:
            await self.session.rollback()

            # A second request could register the same email
            # between our initial check and database insertion.
            existing_user = await self.users.get_by_email(email)

            if existing_user is not None:
                raise EmailAlreadyRegisteredError(
                    "An account with this email already exists."
                )

            # Do not hide unrelated database integrity errors.
            raise

        return user
