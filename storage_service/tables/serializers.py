from django.core.serializers import serialize

from rest_framework import serializers

from tables.models import Table, TableEvent
from schemas.models import Schema
# from utils.producers import KafkaProducer
from grpc_client.client import run_get_views, run_do_migration


# TABLE_CREATE_EVENT_TYPE = 'TableCreated'
# TABLE_UPDATE_EVENT_TYPE = 'TableUpdated'
# TABLE_DELETE_EVENT_TYPE = 'TableDeleted'
#
# producer = KafkaProducer()


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'name', 'schema', 'schema_name']

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        # TableEvent.objects.create(
        #     event_type=TABLE_UPDATE_EVENT_TYPE,
        #     event_data=serialize('json', [instance]),
        # )
        # producer.send_event(TABLE_UPDATE_EVENT_TYPE, serialize('json', [instance]))

        return instance


class TableCreateSerializer(TableSerializer):
    schema_id = serializers.UUIDField(write_only=True)

    class Meta(TableSerializer.Meta):
        fields = [
            'id', 'name', 'schema_id', 'schema_name'
        ]
        read_only_fields = ['id', 'schema_name']

    def create(self, validated_data):
        schema = Schema.objects.get(pk=validated_data['schema_id'])
        instance = Table.objects.create(
            schema=schema,
            schema_name=schema.name,
            **validated_data
        )
        # TableEvent.objects.create(
        #     event_type=TABLE_CREATE_EVENT_TYPE,
        #     event_data=serialize('json', [instance]),
        # )
        # producer.send_event(
        #     TABLE_CREATE_EVENT_TYPE,
        #     serialize('json', [instance])
        # )

        return instance


class TableViewSerializer(TableSerializer):
    row = serializers.IntegerField(write_only=True)

    class Meta(TableSerializer.Meta):
        fields = [
            'id', 'name', 'vendor', 'uri', 'schema_name',
            'column_list', 'row'
        ]
        read_only_fields = [
            'id', 'name', 'vendor', 'uri', 'schema_name', 'column_list'
        ]

    def _convert_to_dict(self, columns, rows):
        response = []
        for row in rows:
            data = {}
            for i in range(len(columns)):
                data[columns[i]] = row[i]
            response.append(data)

        return response

    def create(self, validated_data):
        vendor = self.instance.vendor
        uri = self.instance.uri
        schema = self.instance.schema_name
        table = self.instance.name
        columns = self.instance.column_list
        row = self.validated_data['row']
        rows = run_get_views(
            vendor=vendor,
            uri=uri,
            schema=schema,
            table=table,
            row=row,
            columns=columns
        )
        response = {
            'columns': columns,
            'records': self._convert_to_dict(columns, rows)
        }

        return response

    def save(self):
        return self.create(self.validated_data)


class TableMigrationSerializer(TableSerializer):
    destination_schema = serializers.UUIDField(write_only=True)

    class Meta(TableSerializer.Meta):
        fields = [
            'id', 'name', 'uri', 'destination_schema'
        ]
        read_only_fields = ['id', 'name', 'uri']

    def create(self, validated_data):
        destination_schema = Schema.objects.get(id=validated_data['destination_schema'])
        message = run_do_migration(
            source_uri=self.instance.uri,
            destination_uri=destination_schema.uri,
            table=self.instance.name
        )

        return message

    def save(self):
        return self.create(self.validated_data)


class TableEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableEvent
        fields = ['id', 'event_type', 'event_data', 'created_at']
