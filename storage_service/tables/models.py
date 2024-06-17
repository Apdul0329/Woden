from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import UUIDBaseModel, BaseEventModel, BaseModel


class Table(UUIDBaseModel):
    name = models.CharField(_('name'), max_length=128)
    schema = models.ForeignKey(
        'schemas.Schema', on_delete=models.CASCADE,
        verbose_name=_('schema'),
        help_text=_('Select a schema')
    )
    schema_name = models.CharField(_('schema name'), max_length=128)

    @property
    def vendor(self):
        return self.schema.storage.vendor

    @property
    def uri(self):
        return self.schema.storage.uri

    @property
    def column_list(self):
        return [column.name for column in self.column_set.all()]

    class Meta:
        verbose_name = _('table')


class TableEvent(BaseEventModel):
    class Meta:
        verbose_name = _('table event')
