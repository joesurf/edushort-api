from datetime import datetime, timezone

from app.models.tortoise import Tool


def test_tool_attributes():
    """
    GIVEN url, description, created_at
    WHEN Tool is initialized
    THEN it has attributes with the same values as provided
    """

    today = datetime.now(tz=timezone.utc)

    tool = Tool(
        url="https://www.gmail.com",
        description="Google Mail",
        created_at=today,
    )

    assert tool.url == "https://www.gmail.com"
    assert tool.description == "Google Mail"
    assert tool.created_at == today
