from tortoise import fields
from tortoise.models import Model


class User(Model):
    """User table"""

    id = fields.BigIntField(pk=True)  # same as https://discordpy.readthedocs.io/en/latest/api.html#discord.User.id
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    links: fields.ReverseRelation["PoapLink"]

    def __str__(self):
        return f"#{self.id}"


class PoapLink(Model):
    """POAP pink table"""

    id = fields.UUIDField(pk=True)
    owner = fields.ForeignKeyField("app.User", related_name="links", null=True)
    url = fields.CharField(max_length=255, unique=True)  # poap links should be short
    is_activated = fields.BooleanField(default=False)

    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return self.url
