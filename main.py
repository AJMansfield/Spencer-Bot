#!/usr/bin/env python
"""Run the django bot daemon."""
import os
import sys
from datetime import datetime

from asgiref.sync import sync_to_async

import discord
from discord import Reaction, RawReactionActionEvent
from discord.abc import User

from roles.models import Assignment, Expiry

#TODO how to handle obsoleted expiries?
# user should have a role as long as there are unexpired assignments for that role
#Expiry.objects.filter(user=payload.member, assignment=assignment).delete()

class SpencerClient(discord.Client):
    def __init__(self):
        pass
        
    async def on_raw_reaction_add(self, payload:RawReactionActionEvent):
        now = datetime.now()

        assignments = Assignment.objects.filter(message=payload.message_id, emoji=payload.emoji)
        async for assignment in assignments:
            expiry = Expiry(user=payload.member, assignment=assignment, when=now+assignment.duration)
            await sync_to_async(expiry.save)
            await payload.user.add_roles(assignment.role)
        
    # async def on_raw_reaction_remove(self, payload:RawReactionActionEvent):
    #     now = datetime.now()

    #     assignments = Assignment.objects.filter(message=payload.message_id, emoji=payload.emoji)
    #     async for assignment in assignments:
    #         expiries = Expiry.objects.filter(user=payload.member, assignment=assignment)


    #         await user.remove_roles(discord.Object(assignment.role_id))
    #         await self.dal.complete_assignment_expiry(assignment, user)

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spencer.settings')

