from typing import List, Union
from uuid import UUID

from app.models.tortoise import User

from app.models.models_pydantic.user_pydantic import (  # isort:skip
    UserPayloadSchema,
    UserUpdatePayloadSchema,
)


async def post(payload: UserPayloadSchema) -> UUID:
    user = User(
        email=payload.email,
    )
    await user.save()
    return user.id


async def get(id: UUID) -> Union[dict, None]:
    user = await User.filter(id=id).first().values()
    if user:
        return user
    return None


async def get_all() -> List:
    users = await User.all().values()
    return users


async def delete(id: UUID) -> UUID:
    user = await User.filter(id=id).first().delete()
    return user


async def put(id: UUID, payload: UserUpdatePayloadSchema) -> Union[dict, None]:
    user = await User.filter(id=id).update(credits=payload.credits)
    if user:
        updated_user = await User.filter(id=id).first().values()
        return updated_user
    return None
