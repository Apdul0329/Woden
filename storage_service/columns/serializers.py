from django.core.serializers import serialize

from rest_framework import serializers

from columns.models import Column, ColumnEvent
from tables.models import Table
# from utils.producers import KafkaProducer

#
# COLUMN_CREATE_EVENT_TYPE = 'ColumnCreated'
# COLUMN_UPDATE_EVENT_TYPE = 'ColumnUpdated'
# COLUMN_DELETE_EVENT_TYPE = 'ColumnDeleted'
#
# producer = KafkaProducer()


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ['id', 'name', 'type', 'details', 'table']

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        # ColumnEvent.objects.create(
        #     event_type=COLUMN_UPDATE_EVENT_TYPE,
        #     event_data=serialize('json', [instance]),
        # )
        # producer.send_event(COLUMN_UPDATE_EVENT_TYPE, serialize('json', [instance]))

        return instance


class ColumnCreateSerializer(ColumnSerializer):
    table_id = serializers.UUIDField(write_only=True)

    class Meta(ColumnSerializer.Meta):
        fields = [
            'id', 'name', 'type', 'details', 'table_id',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        table = Table.objects.get(pk=validated_data['table_id'])
        instance = Column.objects.create(
            table=table,
            **validated_data
        )
        # ColumnEvent.objects.create(
        #     event_type=COLUMN_CREATE_EVENT_TYPE,
        #     event_data=serialize('json', [instance]),
        # )
        # producer.send_event(
        #     COLUMN_CREATE_EVENT_TYPE,
        #     serialize('json', [instance])
        # )

        return instance


class ColumnEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColumnEvent
        fields = ['id', 'event_type', 'event_data', 'created_at']