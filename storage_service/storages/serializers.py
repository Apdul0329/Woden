from django.core.serializers import serialize

from rest_framework import serializers

from storages.models import Storage, StorageEvent
# from utils.producers import KafkaProducer
from storages.tasks import get_schemas_task

# STORAGE_CREATE_EVENT_TYPE = 'StorageCreated'
# STORAGE_UPDATE_EVENT_TYPE = 'StorageUpdated'
# STORAGE_DELETE_EVENT_TYPE = 'StorageDeleted'
#
# producer = KafkaProducer()


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = [
            'id', 'name', 'vendor', 'username', 'password',
            'host', 'port', 'owner_id', 'group_id'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        instance = super().create(validated_data)
        # StorageEvent.objects.create(
        #     event_type=STORAGE_CREATE_EVENT_TYPE,
        #     event_data=serialize('json', [instance]),
        # )
        # producer.send_event(
        #     STORAGE_CREATE_EVENT_TYPE,
        #     serialize('json', [instance])
        # )
        get_schemas_task.delay(
            id=str(instance.id),
            vendor=instance.vendor,
            uri=instance.uri
        )

        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        # StorageEvent.objects.create(
        #     event_type=STORAGE_UPDATE_EVENT_TYPE,
        #     event_data=serialize('json', [instance]),
        # )
        # producer.send_event(STORAGE_UPDATE_EVENT_TYPE, serialize('json', [instance]))

        return instance


class StorageEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageEvent
        fields = ['id', 'event_type', 'event_data', 'created_at']
