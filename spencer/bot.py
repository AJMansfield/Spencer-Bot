import asyncio
from datetime import datetime
from typing import Union, Tuple
import discord
from discord import Reaction, Member, User, Emoji, partial_emoji
import sqlalchemy

from spencer.dal import DAL


# def id_str_to_emoji(id:int = 0, str_:str = '') -> Union[Emoji, PartialEmoji, str]:

class SpencerClient(discord.Client):
    def __init__(self, db_session:sqlalchemy.orm.Session):
        self.dal = DAL(self, db_session)
        
    async def on_reaction_add(self, reaction:Reaction, user:Union[Member, User]):
        now = datetime.now()

        assignments = await self.dal.get_assignments(reaction)
        async for assignment in assignments:
            await self.dal.create_expiry(assignment, user, now + assignment.duration)
            await user.add_roles(discord.Object(assignment.role_id))
        
    async def on_reaction_remove(self, reaction:Reaction, user:Union[Member, User]):
        now = datetime.now()

        assignments = await self.dal.get_assignments(reaction)
        async for assignment in assignments:
            await user.remove_roles(discord.Object(assignment.role_id))
            await self.dal.complete_assignment_expiry(assignment, user)
    
    
