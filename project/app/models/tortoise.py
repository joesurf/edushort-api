from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class User(models.Model):
    id = fields.UUIDField(pk=True)
    email = fields.CharField(unique=True, max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    credits = fields.SmallIntField(default=0)

    def __str__(self):
        return self.email


UserSchema = pydantic_model_creator(User)


class Video(models.Model):
    id = fields.UUIDField(pk=True)
    url = fields.TextField(default="")
    title = fields.TextField(default="")
    description = fields.TextField(default="")
    script = fields.TextField(default="")
    created_at = fields.DatetimeField(auto_now_add=True)
    author = fields.ForeignKeyField(
        model_name="models.User",
        related_name="Created",
        on_delete=fields.CASCADE,
        null=True,
    )

    def __str__(self):
        return self.id


VideoSchema = pydantic_model_creator(Video)
