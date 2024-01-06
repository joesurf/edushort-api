from uuid import UUID

from app.animator.main import generate_video_locally

# TODO: implement auto saving using useeffect with PUT_CONTENT + OpenAI moderation

# TODO: Send email update - input [user id] output [boolean success]
# TODO: Update credits - input [user id] output [credits]


def generate_video_from_script(id: UUID, script: str) -> None:
    generate_video_locally(video_id=str(id), script=script)
