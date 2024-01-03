from fastapi import APIRouter

router = APIRouter()


@router.get("/{id}/")
async def get_user(id: int):
    pass


@router.get("/")
async def get_all_users():
    pass


@router.post("/")
async def add_user():
    pass


@router.put("/{id}")
async def update_user():
    pass


@router.delete("/{id}")
async def delete_user():
    pass
