import uuid
# from dateutil import parser

from django_extensions.db.models import TimeStampedModel
from django.db import models
from django.utils.translation import gettext_lazy as _

import logging

logger = logging.getLogger(__name__)

# Create your models here.


class BaseModelManager(models.Manager):
    def get_queryset(self):
        return super(BaseModelManager, self).get_queryset().filter(is_deleted=False)


# Create your models here.
class BaseModel(TimeStampedModel):
    """Base model - have common fields to all models."""
    # unique key to each record
    # maintaining uuid as primary key can be expensive, hence we will use uuid as secondary key as external identifier.
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    # deletion attributes
    is_deleted = models.BooleanField(default=False, db_index=True)

    # overriding django model managers
    objects = BaseModelManager()  # overriding the django's object manager to filter out deleted records.
    all_objects = models.Manager()  # exposing all the objects including the soft deleted records.

    def hard_delete(self, *args, **kwargs):
        """hard delete which exposes actual delete from database"""
        super(BaseModel, self).delete(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """soft delete enforced for all models """
        self.is_deleted = True
        super().save()

    class Meta:
        abstract = True

    def __unicode__(self):
        return "%s" % self.uuid

    def __str__(self):
        return "{}".format(self.uuid)



class Game(BaseModel):
    """
       Game saves state of game.
    """

    upcoming_move_sequence_number = models.IntegerField(
        verbose_name='Sequence Number of Next Move',
        null=False, blank=False, default=1
    )

    YELLOW = 'YELLOW'
    RED = 'RED'
    WINNER_COLOR_CHOICES = [
        (YELLOW, _('Yellow')),
        (RED, _('Red')),
    ]

    winner_color = models.CharField(
        verbose_name='Winner of Game',
        null=True, blank=True,
        choices=WINNER_COLOR_CHOICES,
        max_length=100,
    )

    def __str__(self):
        return f"Game[uuid={self.uuid} winner={self.winner} next_move: {self.upcoming_move_seq}]"


class Move(BaseModel):
    """
        Move represent move of a game.
    """

    game = models.ForeignKey(
        Game,
        verbose_name='Game',
        related_name='moves',
        null=False, blank=False, on_delete=models.CASCADE,
    )

    column = models.IntegerField(
        verbose_name='Column',
        null=False, blank=False
    )

    row = models.IntegerField(
        verbose_name='row',
        null=False, blank=False
    )

    YELLOW = 'YELLOW'
    RED = 'RED'
    PLAYER_COLOR_CHOICES = [
        (YELLOW, _('Yellow')),
        (RED, _('Red')),
    ]

    player_color = models.CharField(
        verbose_name='Player of Move',
        null=False, blank=False,
        choices=PLAYER_COLOR_CHOICES,
        max_length=100,
    )

    sequence_number = models.IntegerField(
        verbose_name='Sequence Number',
        null=False, blank=False
    )

