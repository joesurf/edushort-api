from typing import List

from fastapi import APIRouter, HTTPException, Path

from app.api import tools_crud
from app.models.pydantic import (ToolPayloadSchema, ToolResponseSchema,
                                 ToolUpdatePayloadSchema)
from app.models.tortoise import ToolSchema

router = APIRouter()


@router.post("/", response_model=ToolResponseSchema, status_code=201)
async def create_Tool(payload: ToolPayloadSchema) -> ToolResponseSchema:
    tool_id = await tools_crud.post(payload)

    response_object = {"id": tool_id, "url": payload.url}
    return response_object


@router.get("/{id}/", response_model=ToolSchema)
async def get_tool(id: int = Path(..., gt=0)) -> ToolSchema:
    tool = await tools_crud.get(id)

    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")

    return tool


@router.get("/", response_model=List[ToolSchema])
async def get_all_tools() -> List[ToolSchema]:
    tools = await tools_crud.get_all()

    return tools


@router.delete("/{id}/", response_model=ToolResponseSchema)
async def delete_tool(id: int = Path(..., gt=0)) -> ToolResponseSchema:
    tool = await tools_crud.get(id)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")

    await tools_crud.delete(id)

    return tool


@router.put("/{id}/", response_model=ToolSchema)
async def update_tool(
    payload: ToolUpdatePayloadSchema, id: int = Path(..., gt=0)
) -> ToolSchema:
    tool = await tools_crud.put(id, payload)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")

    return tool
