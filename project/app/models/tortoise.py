from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Tool(models.Model):
    url = fields.TextField()
    description = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.url


ToolSchema = pydantic_model_creator(Tool)
