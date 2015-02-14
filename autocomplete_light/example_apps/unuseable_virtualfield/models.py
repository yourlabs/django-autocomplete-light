from django.db import models

from vote.managers import VotableManager


class HasVotes(models.Model):
    votes = VotableManager()
