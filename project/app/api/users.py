from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.api import users_crud
from app.models.tortoise import UserSchema

from app.models.models_pydantic.user_pydantic import (  # isort:skip
    UserPayloadSchema,
    UserResponseSchema,
    UserUpdatePayloadSchema,
)

router = APIRouter()


@router.post("/", response_model=UserResponseSchema, status_code=201)
async def add_user(payload: UserPayloadSchema) -> UserResponseSchema:
    user_id = await users_crud.post(payload)

    response_object = {"id": user_id, "email": payload.email}
    return response_object


@router.get("/{id}/", response_model=UserSchema)
async def get_user(id: UUID) -> UserSchema:
    user = await users_crud.get(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.get("/", response_model=List[UserSchema])
async def get_all_users() -> List[UserSchema]:
    users = await users_crud.get_all()

    return users


@router.put("/{id}/", response_model=UserSchema)
async def update_user(id: UUID, payload: UserUpdatePayloadSchema) -> UserSchema:
    user = await users_crud.put(id, payload)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.delete("/{id}/", response_model=UserResponseSchema)
async def delete_user(id: UUID) -> UserResponseSchema:
    user = await users_crud.get(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await users_crud.delete(id)

    return user
