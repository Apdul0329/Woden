import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    added_at = models.DateTimeField(_('added at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    deleted_at = models.DateTimeField(_('deleted at'), null=True, editable=False)

    class Meta:
        abstract = True


class UUIDBaseModel(BaseModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        verbose_name=_('ID')
    )

    class Meta:
        abstract = True


class BaseEventModel(models.Model):
    event_type = models.CharField(_('event type'), max_length=128)
    event_data = models.JSONField()
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        abstract = True
