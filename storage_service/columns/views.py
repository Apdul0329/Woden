import gzip
import json

from rest_framework import viewsets, status
from rest_framework.response import Response

from columns.models import Column, ColumnEvent
from columns.serializers import (
    ColumnSerializer, ColumnCreateSerializer,
    # COLUMN_DELETE_EVENT_TYPE, producer
)
from utils.mixins import StreamParser


class ColumnViewSet(viewsets.ModelViewSet):
    queryset = Column.objects.all()
    serializer_class = ColumnSerializer
    parser_classes = [StreamParser]

    def get_serializer_class(self):
        if self.action == 'create':
            return ColumnCreateSerializer
        else:
            return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        if request.content_type == 'application/json-stream':
            return self._handle_stream(request)
        else:
            serializer = self.get_serializer(data=request.data, many=True, **kwargs)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _handle_stream(self, request):
        bulk_data = []
        parsed_data = request.data

        for data in parsed_data:
            serializer = ColumnCreateSerializer(data=data)
            if serializer.is_valid():
                bulk_data.append(Column(**serializer.validated_data))
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        Column.objects.bulk_create(bulk_data)
        return Response({'message': 'Data uploaded successfully'}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # event_data = {
        #     'id': str(instance.id)
        # }
        response = super().destroy(request, *args, **kwargs)
        # if response.status_code == status.HTTP_204_NO_CONTENT:
        #     ColumnEvent.objects.create(
        #         event_type=COLUMN_DELETE_EVENT_TYPE,
        #         event_data=event_data,
        #     )
        #     producer.send_event(COLUMN_DELETE_EVENT_TYPE, event_data)
        return response