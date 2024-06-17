from django.core.serializers import serialize

from rest_framework import viewsets, status
from rest_framework.response import Response

from schemas.models import Schema, SchemaEvent
from schemas.tasks import get_tables_task
from schemas.serializers import (
    SchemaSerializer, SchemaCreateSerializer,
    # SCHEMA_DELETE_EVENT_TYPE, producer
)


class SchemaViewSet(viewsets.ModelViewSet):
    queryset = Schema.objects.all()
    serializer_class = SchemaSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return SchemaCreateSerializer
        else:
            return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()
        storage_id = self.request.query_params.get('storage')
        if storage_id:
            queryset = queryset.filter(storage_id=storage_id)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True, **kwargs)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance = serializer.instance[0]
        get_tables_task.delay(
            vendor=instance.vendor,
            uri=instance.uri,
            schemas=serialize('json', serializer.instance)
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # event_data = {
        #     'id': str(instance.id)
        # }
        response = super().destroy(request, *args, **kwargs)
        # if response.status_code == status.HTTP_204_NO_CONTENT:
        #     SchemaEvent.objects.create(
        #         event_type=SCHEMA_DELETE_EVENT_TYPE,
        #         event_data=event_data,
        #     )
        #     producer.send_event(SCHEMA_DELETE_EVENT_TYPE, event_data)
        return response
