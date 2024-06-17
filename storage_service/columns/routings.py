from django.urls import path

from columns.consumer import ColumnConsumer


websocket_urlpatterns = [
    path('ws/columns/<uuid:pk>/', ColumnConsumer.as_asgi()),
]