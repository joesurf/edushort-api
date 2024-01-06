from uuid import UUID

from pydantic import AnyHttpUrl

from app.animator.main import generate_video_locally

# TODO: implement auto saving using useeffect with PUT_CONTENT + OpenAI moderation

# TODO: Send email update - input [user id] output [boolean success]
# TODO: Update credits - input [user id] output [credits]

async def generate_video_from_script(id: UUID, script: str) -> AnyHttpUrl:
    generate_video_locally(
        video_id=str(id),
        script=script
    )

    return f"https://s3.amazonaws.com/edushort.joesurf.io/media/videos/{id}.mp4"
