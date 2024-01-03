from fastapi import APIRouter


router = APIRouter()


@router.get("/{id}/")
async def get_video(id: int):
    pass


@router.get("/")
async def get_all_videos():
    pass


@router.post("/")
async def get_video():
    pass


@router.put("/{id}")
async def update_video():
    pass


@router.delete("/{id}")
async def delete_video():
    pass
