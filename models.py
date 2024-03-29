from tortoise import models, fields
from tortoise.contrib.pydantic import pydantic_model_creator


class Users(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    name = fields.CharField(max_length=50, null=True)
    family_name = fields.CharField(max_length=50, null=True)
    password_hash = fields.CharField(max_length=30, null=True)
    created_at = fields.DatetimeField(auto_now_add=True, null=True)
    updated_at = fields.DatetimeField(auto_now=True, null=True)

    def full_name(self) -> str:
        if self.name or self.family_name:
            return f"{self.name or ''} {self.family_name or ''}".strip()
        return self.username

    class Meta:
        table = 'user'

    class PydanticMeta:
        computed = ['full_name']
        exclude = ['password_hash']


User_Pydantic = pydantic_model_creator(Users, name='User')
UserIn_Pydantic = pydantic_model_creator(Users, name='UserIn', exclude=('created_at', 'updated_at'),
                                         exclude_readonly=True)
