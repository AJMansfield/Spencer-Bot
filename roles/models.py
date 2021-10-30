from django.db import models

from roles.fields import DiscordObjectField

class Assignment(models.Model):
    message = DiscordObjectField()
    emoji = DiscordObjectField()
    role = DiscordObjectField()
    duration = models.DurationField()

class Expiry(models.Model):
    user = DiscordObjectField()
    assignment = models.ForeignKey(Assignment, on_delete=models.RESTRICT)
    # TODO create a callback thing to resolve expiries when trying to delete an Assignment
    when = models.DateTimeField()