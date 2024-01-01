from typing import List, Union

from app.models.pydantic import ToolPayloadSchema
from app.models.tortoise import Tool


async def post(payload: ToolPayloadSchema) -> int:
    tool = Tool(
        url=payload.url,
        description="dummy tool",
    )
    await tool.save()
    return tool.id


async def get(id: int) -> Union[dict, None]:
    tool = await Tool.filter(id=id).first().values()
    if tool:
        return tool
    return None


async def get_all() -> List:
    tools = await Tool.all().values()
    return tools


async def delete(id: int) -> int:
    summary = await Tool.filter(id=id).first().delete()
    return summary


async def put(id: int, payload: ToolPayloadSchema) -> Union[dict, None]:
    summary = await Tool.filter(id=id).update(
        url=payload.url, description=payload.description
    )
    if summary:
        updated_summary = await Tool.filter(id=id).first().values()
        return updated_summary
    return None
