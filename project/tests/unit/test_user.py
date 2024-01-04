from datetime import datetime, timezone
from uuid import uuid4

from app.models.tortoise import User


def test_user_attributes():
    """
    GIVEN id, email, credits, created_at
    WHEN User is initialized
    THEN it has attributes with the same values as provided
    """

    today = datetime.now(tz=timezone.utc)
    user_id = uuid4()

    user = User(
        id=user_id,
        email="test@gmail.com",
        credits=5,
        created_at=today,
    )

    assert user.id == user_id
    assert user.email == "test@gmail.com"
    assert user.credits == 5
    assert user.created_at == today
