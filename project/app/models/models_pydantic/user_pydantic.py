from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserPayloadSchema(BaseModel):
    email: EmailStr


class UserResponseSchema(UserPayloadSchema):
    id: UUID


class UserUpdatePayloadSchema(UserPayloadSchema):
    credits: int
