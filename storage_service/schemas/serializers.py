from django.core.serializers import serialize

from rest_framework import serializers

from schemas.models import Schema, SchemaEvent
from storages.models import Storage
# from utils.producers import KafkaProducer

# SCHEMA_CREATE_EVENT_TYPE = 'SchemaCreated'
# SCHEMA_UPDATE_EVENT_TYPE = 'SchemaUpdated'
# SCHEMA_DELETE_EVENT_TYPE = 'SchemaDeleted'
#
# producer = KafkaProducer()


class SchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schema
        fields = ['id', 'name', 'storage']

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        # SchemaEvent.objects.create(
        #     event_type=SCHEMA_UPDATE_EVENT_TYPE,
        #     event_data=serialize('json', [instance]),
        # )
        # producer.send_event(SCHEMA_UPDATE_EVENT_TYPE, serialize('json', [instance]))

        return instance


class SchemaCreateSerializer(SchemaSerializer):
    storage_id = serializers.UUIDField(write_only=True)

    class Meta(SchemaSerializer.Meta):
        fields = [
            'id', 'name', 'storage_id'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        storage = Storage.objects.get(pk=validated_data['storage_id'])
        instance = Schema.objects.create(
            storage=storage,
            **validated_data
        )
        # SchemaEvent.objects.create(
        #     event_type=SCHEMA_CREATE_EVENT_TYPE,
        #     event_data=serialize('json', [instance]),
        # )
        # producer.send_event(
        #     SCHEMA_CREATE_EVENT_TYPE,
        #     serialize('json', [instance])
        # )

        return instance


class SchemaEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchemaEvent
        fields = ['id', 'event_type', 'event_data', 'created_at']
