from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.api import videos_crud
from app.api.videos_helper import generate_video_from_script

from app.models.models_pydantic.video_pydantic import (  # isort:skip
    VideoPayloadSchema,
    VideoResponseSchema,
    VideoUpdatePayloadSchema,
    VideoFullResponseSchema,
)


router = APIRouter()


@router.post("/", response_model=VideoResponseSchema, status_code=201)
async def add_video(payload: VideoPayloadSchema) -> VideoResponseSchema:
    video_id = await videos_crud.post(payload)

    response_object = {"id": video_id, "author_id": payload.author_id}
    return response_object


@router.get("/{id}/", response_model=VideoFullResponseSchema)
async def get_video(id: UUID) -> VideoFullResponseSchema:
    video = await videos_crud.get(id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    return video


@router.get("/", response_model=List[VideoFullResponseSchema])
async def get_all_videos() -> List[VideoFullResponseSchema]:
    videos = await videos_crud.get_all()
    return videos


@router.put("/{id}/", response_model=VideoFullResponseSchema)
async def update_video(
    id: UUID, payload: VideoUpdatePayloadSchema
) -> VideoFullResponseSchema:
    video = await videos_crud.put_content(id, payload)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    return video


@router.delete("/{id}/", response_model=VideoResponseSchema)
async def delete_video(id: UUID) -> VideoResponseSchema:
    video = await videos_crud.get(id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    await videos_crud.delete(id)

    return video


# higher order routes
@router.post("/{id}/", response_model=VideoFullResponseSchema, status_code=201)
async def generate_video(id: UUID) -> VideoFullResponseSchema:
    video = await videos_crud.get(id)

    if not video["title"] or not video["script"]:
        raise HTTPException(status_code=404, detail="Missing fields [title, script]")

    video_url = await generate_video_from_script(video["script"])

    video = await videos_crud.put_link(id, {"url": video_url})
    return video
