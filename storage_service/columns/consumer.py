import json
import uuid
import asyncio
import redis

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from storage_service.settings import REDIS_HOST, REDIS_PORT

from columns.serializers import ColumnCreateSerializer
from columns.models import Column


class ColumnConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.redis_client = redis.StrictRedis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=1
        )
        self.uuid = str(self.scope['url_route']['kwargs']['pk'])
        await self.accept()

    async def receive_json(self, content):
        if content.get('signal') == 'END':
            await self.perform_bulk_insert(self.uuid)
        else:
            self.redis_client.rpush(
                self.uuid,
                json.dumps(content)
            )

    async def disconnect(self, close_code):
        pass

    async def perform_bulk_insert(self, uuid):
        bulk_data = []
        columns = self.redis_client.lrange(uuid, 0, -1)

        for column in columns:
            serializer = ColumnCreateSerializer(data=json.loads(column))
            if serializer.is_valid():
                bulk_data.append(Column(**serializer.validated_data))

        await database_sync_to_async(
            Column.objects.bulk_create
        )(bulk_data)
