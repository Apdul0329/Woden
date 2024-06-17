from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import UUIDBaseModel, BaseEventModel, BaseModel


class Column(BaseModel):
    name = models.CharField(_('name'), max_length=128)
    type = models.CharField(_('type'), max_length=128)
    details = models.JSONField(_('details'), blank=True)
    table = models.ForeignKey(
        'tables.Table', on_delete=models.CASCADE,
        verbose_name=_('table'),
        help_text=_('Select a table')
    )

    class Meta:
        verbose_name = _('column')


class ColumnEvent(BaseEventModel):
    class Meta:
        verbose_name = _('column event')
