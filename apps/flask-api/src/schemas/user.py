from marshmallow import ValidationError, fields, validate, validates_schema

from src.extensions import ma
from src.models.user import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    """Schema for user serialization."""

    class Meta:
        model = User
        load_instance = True
        exclude = ("password_hash",)


class UserCreateSchema(ma.Schema):
    """Schema for user registration."""

    username = fields.String(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    password = fields.String(
        required=True, validate=validate.Length(min=8), load_only=True
    )
    password_confirm = fields.String(required=True, load_only=True)

    @validates_schema
    def validate_passwords(self, data, **kwargs):
        if data["password"] != data["password_confirm"]:
            raise ValidationError({"password_confirm": "Passwords do not match."})


class UserUpdateSchema(ma.Schema):
    """Schema for updating user profile."""

    phone_number = fields.String()
    bio = fields.String()
    avatar = fields.String()
    theme = fields.String(validate=validate.OneOf(["light", "dark"]))
    email_notifications = fields.Boolean()


class LoginSchema(ma.Schema):
    """Schema for user login."""

    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)


class ChangePasswordSchema(ma.Schema):
    """Schema for password change."""

    old_password = fields.String(required=True, load_only=True)
    new_password = fields.String(
        required=True, validate=validate.Length(min=8), load_only=True
    )
    new_password_confirm = fields.String(required=True, load_only=True)

    @validates_schema
    def validate_passwords(self, data, **kwargs):
        if data["new_password"] != data["new_password_confirm"]:
            raise ValidationError({"new_password_confirm": "Passwords do not match."})
