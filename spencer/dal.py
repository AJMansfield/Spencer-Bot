
from datetime import datetime
from typing import Sequence, Union, Tuple
from dataclasses import dataclass

import sqlalchemy
from sqlalchemy.future import select
from sqlalchemy.sql.expression import Select, and_, or_, not_
import discord

from spencer.models import Assignment, Expiry

def emoji_to_id_str(emoji: Union[discord.Emoji, discord.PartialEmoji, str]) -> tuple[int, str]:
    try:
        return (emoji.id, '')
    except AttributeError:
        return (0, emoji)

@dataclass
class DAL():
    db_session : sqlalchemy.orm.Session
    dis_client : discord.Client

    async def get_assignments(self, reaction: discord.Reaction) -> list[Assignment]:
        emoji_id, emoji_str = emoji_to_id_str(reaction.emoji)
        q: Select = select(Assignment)
        q = q.where(Assignment.message_id == reaction.message.id)
        q = q.where(Assignment.emoji_id == emoji_id)
        q = q.where(Assignment.emoji_str == emoji_str)
        result = await self.db_session.execute(q)
        return result.scalars().all()
    
    async def create_expiry(self, assignment: Assignment, user: discord.User, when: datetime):
        new_expiry = Expiry(user_id = user.id, assignment = assignment, when = when, complete = False)
        self.db_session.add(new_expiry)
        await self.db_session.flush()
    
    async def get_ready_expiries(self, now: datetime):
        q: Select = select(Expiry)
        q = q.where(Expiry.when >= now)
        q = q.where(not_(Expiry.complete))
        result = await self.db_session.execute(q)
        return result.scalars().all()



        
