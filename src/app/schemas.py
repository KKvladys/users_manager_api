from marshmallow import Schema, fields, validates
from pydantic import ValidationError

from src.database.validators.users_validators import (
    validate_name,
    validate_email
)


class UserBaseSchema(Schema):
    """
    Base schema for user validation.
    """
    name = fields.Str(required=True)
    email = fields.Email(required=True)

    @validates("name")
    def validate_name(self, name):
        """
        Validate the 'name' field using the `validate_name` function.
        """
        try:
            validate_name(name)
        except ValueError as e:
            raise ValidationError(str(e))

    @validates("email")
    def validate_email(self, email):
        """
        Validate the 'email' field using the `validate_email` function.
        """
        try:
            validate_email(email)
        except ValueError as e:
            raise ValidationError(str(e))


class UserCreateSchema(UserBaseSchema):
    """
    Schema for user creation.
    """
    pass


class UserUpdateSchema(UserBaseSchema):
    """
    Schema for user update.
    """
    pass


class UserResponseSchema(UserBaseSchema):
    """
    Schema for user response data.
    """
    name = fields.Str(dump_only=True)
    email = fields.Email(dump_only=True)
    created_at = fields.DateTime(dump_only=True)


user_create_schema = UserCreateSchema()
user_update_schema = UserUpdateSchema()
user_response_schema = UserResponseSchema()
