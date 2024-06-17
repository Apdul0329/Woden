from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import UUIDBaseModel, BaseEventModel


class Schema(UUIDBaseModel):
    name = models.CharField(_('name'), max_length=128)
    storage = models.ForeignKey(
        'storages.Storage', on_delete=models.CASCADE,
        verbose_name=_('storage'),
        help_text=_('Select a storage')
    )

    @property
    def vendor(self):
        return self.storage.vendor

    @property
    def uri(self):
        return self.storage.uri

    class Meta:
        verbose_name = _('schema')


class SchemaEvent(BaseEventModel):
    class Meta:
        verbose_name = _('schema event')
