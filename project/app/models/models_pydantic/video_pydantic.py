from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class VideoPayloadSchema(BaseModel):
    author_id: Optional[UUID] = None


class VideoUpdatePayloadSchema(BaseModel):
    title: str
    description: str
    script: str


class VideoGenerationPayloadSchema(BaseModel):
    url: str


class VideoResponseSchema(VideoPayloadSchema):
    id: UUID


class VideoFullResponseSchema(
    VideoUpdatePayloadSchema, VideoGenerationPayloadSchema, VideoResponseSchema
):
    created_at: datetime
