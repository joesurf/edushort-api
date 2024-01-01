from pydantic import AnyHttpUrl, BaseModel


class ToolPayloadSchema(BaseModel):
    url: AnyHttpUrl


class ToolResponseSchema(ToolPayloadSchema):
    id: int


class ToolUpdatePayloadSchema(ToolPayloadSchema):
    description: str
