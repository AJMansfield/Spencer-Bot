from django.db import models
from django.core.exceptions import ValidationError
from typing import Union, Optional
import discord

class DiscordObjectField(models.IntegerField):
    description = "An arbitrary discord.Object."
    def _make_obj(self, id:int):
        return discord.Object(id)

    def from_db_value(self, value, expression, connection)-> Optional[discord.Object]:
        if value is None:
            return value
        return self._make_obj(value)

    def to_python(self, value:Optional[Union[discord.Object,int]]) -> Optional[discord.Object]:
        if value is None:
            return value
        elif isinstance(value, discord.Object):
            return value
        elif isinstance(value, int):
            return self._make_obj(value)
        else:
            raise ValidationError(f'{value!r} is not a valid discord.Object id')
    
    def get_prep_value(self, value:Optional[discord.Object]) -> Optional[int]:
        if value is None:
            return value
        else:
            try:
                return value.id
            except AttributeError as e:
                raise ValidationError from e
