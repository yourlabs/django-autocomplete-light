from django.db import models

from .vote_models import VotableManager


class HasVotes(models.Model):
    votes = VotableManager()
