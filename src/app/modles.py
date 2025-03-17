from datetime import datetime

from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, validates

from src.database.database import db
from src.database.validators.users_validators import (
    validate_name,
    validate_email
)


class User(db.Model):
    """
    User model for storing user information in the database.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        """Return string representation of the user."""
        return f"<User {self.name}, email: {self.email}>"

    @validates("name")
    def validate_name(self, key, name: str) -> str:
        return validate_name(name)

    @validates("email")
    def validate_email(self, key, email: str) -> str:
        return validate_email(email)

    @classmethod
    def create(cls, name: str, email: str, password: str) -> "User":
        """
        Create a new user instance.
        """
        new_user = cls(name=name, email=email)
        new_user.password = password
        return new_user
