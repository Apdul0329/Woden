import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import UUIDBaseModel, BaseEventModel


VENDOR_CHOICES = [
    ('postgresql', 'PostgreSQL'),
    ('mysql', 'MySQL'),
]


class Storage(UUIDBaseModel):
    name = models.CharField(_('name'), max_length=128)
    vendor = models.CharField(_('vendor'), choices=VENDOR_CHOICES)
    username = models.CharField(_('username'), max_length=128)
    password = models.CharField(
        _('password'),
        null=True, blank=True,
        max_length=128
    )
    host = models.GenericIPAddressField(
        verbose_name=_('host'),
        help_text=_('Enter host.')
    )
    port = models.PositiveIntegerField(_('port'))
    owner_id = models.UUIDField(
        default=uuid.uuid4,
        verbose_name=_('owner ID')
    )
    group_id = models.UUIDField(
        default=uuid.uuid4,
        verbose_name=_('group ID')
    )
    is_connect = models.BooleanField(
        null=True, blank=True,
        default=False,
        verbose_name=_('is connect')
    )

    class Meta:
        verbose_name = _('Storage')

    @property
    def uri(self):
        return f'{self.vendor}://{self.username}:{self.password}@{self.host}:{self.port}/{self.name}'



class StorageEvent(BaseEventModel):
    class Meta:
        verbose_name = _('storage event')
