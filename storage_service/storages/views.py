from rest_framework import viewsets, status
from rest_framework.response import Response

from storages.models import Storage, StorageEvent
from storages.serializers import (
    StorageSerializer,
    # STORAGE_DELETE_EVENT_TYPE, producer
)


class StorageViewSet(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # event_data = {
        #     'id': str(instance.id)
        # }
        response = super().destroy(request, *args, **kwargs)
        # if response.status_code == status.HTTP_204_NO_CONTENT:
            # StorageEvent.objects.create(
            #     event_type=STORAGE_DELETE_EVENT_TYPE,
            #     event_data=event_data,
            # )
            # producer.send_event(STORAGE_DELETE_EVENT_TYPE, event_data)
        return response
