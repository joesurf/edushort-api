from typing import List, Union
from uuid import UUID

from app.models.tortoise import User, Video

from app.models.models_pydantic.video_pydantic import (  # isort:skip
    VideoPayloadSchema,
    VideoUpdatePayloadSchema,
    VideoGenerationPayloadSchema,
    VideoFullResponseSchema,
)


async def post(payload: VideoPayloadSchema) -> UUID:
    user = await User.filter(id=payload.author_id).first()

    video = Video(author=user)
    await video.save()
    return video.id


async def get(id: UUID) -> Union[VideoFullResponseSchema, None]:
    video = await Video.filter(id=id).first().values()
    if video:
        return video
    return None


async def get_all() -> List[VideoFullResponseSchema]:
    videos = await Video.all().values()
    return videos


async def delete(id: UUID) -> UUID:
    video = await Video.filter(id=id).first().delete()
    return video


async def put_content(id: UUID, payload: VideoUpdatePayloadSchema) -> Union[dict, None]:
    video = await Video.filter(id=id).update(
        title=payload.title,
        description=payload.description,
        script=payload.script,
    )

    if video:
        updated_video = await Video.filter(id=id).first().values()
        return updated_video
    return None


async def put_link(
    id: UUID, payload: VideoGenerationPayloadSchema
) -> Union[dict, None]:
    video = await Video.filter(id=id).update(url=payload["url"])

    if video:
        updated_video = await Video.filter(id=id).first().values()
        return updated_video
    return None
