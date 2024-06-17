from django.core.serializers import serialize

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from tables.models import Table, TableEvent
from tables.tasks import get_columns_task
from tables.serializers import (
    TableSerializer, TableCreateSerializer, TableViewSerializer,
    TableMigrationSerializer,
    # TABLE_DELETE_EVENT_TYPE, producer
)


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return TableCreateSerializer
        else:
            return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()
        schema_id = self.request.query_params.get('schema')
        if schema_id:
            queryset = queryset.filter(schema_id=schema_id)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True, **kwargs)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance = serializer.instance[0]
        get_columns_task.delay(
            vendor=instance.vendor,
            uri=instance.uri,
            tables=serialize('json', serializer.instance)
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # event_data = {
        #     'id': str(instance.id)
        # }
        response = super().destroy(request, *args, **kwargs)
        # if response.status_code == status.HTTP_204_NO_CONTENT:
        #     TableEvent.objects.create(
        #         event_type=TABLE_DELETE_EVENT_TYPE,
        #         event_data=event_data,
        #     )
        #     producer.send_event(TABLE_DELETE_EVENT_TYPE, event_data)
        return response

    @action(detail=True, methods=['post'], serializer_class=TableViewSerializer)
    def view(self, request, pk=None):
        serializer = self.get_serializer(
            instance=self.get_object(),
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], serializer_class=TableMigrationSerializer)
    def migration(self, request, pk=None):
        serializer = self.get_serializer(
            instance=self.get_object(),
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        return Response(data=data, status=status.HTTP_200_OK)

