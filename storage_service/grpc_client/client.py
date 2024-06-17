import os
import pickle
import grpc

from django.core.serializers import deserialize

import grpc_client.storages_pb2 as storages_pb2
import grpc_client.storages_pb2_grpc as storages_pb2_grpc
from schemas.models import Schema
# from utils.producers import KafkaProducer

GRPC_SERVER_URL = os.getenv('GRPC_SERVER_URL', 'localhost:50051')

# producer = KafkaProducer()


def run_get_schemas(id, vendor, uri):
    with grpc.insecure_channel(GRPC_SERVER_URL) as channel:
        stub = storages_pb2_grpc.DataSourceManageServiceStub(channel)
        response = stub.GetSchemas(storages_pb2.SchemaRequest(
            id=id,
            vendor=vendor,
            uri=uri,
        ))

        if response.success:
            print(response)


def run_get_tables(vendor, uri, schemas):
    with grpc.insecure_channel(GRPC_SERVER_URL) as channel:
        stub = storages_pb2_grpc.DataSourceManageServiceStub(channel)
        schema_list = [
            storages_pb2.Schema(
                id=str(schema.object.id),
                schema=schema.object.name
            )
            for schema in list(deserialize('json', schemas))
        ]
        response = stub.GetTables(storages_pb2.TableRequest(
            vendor=vendor,
            uri=uri,
            schemas=schema_list,
        ))
        if response.success:
            print(response)


def run_get_columns(vendor, uri, tables):
    with grpc.insecure_channel(GRPC_SERVER_URL) as channel:
        stub = storages_pb2_grpc.DataSourceManageServiceStub(channel)
        table_list = [
            storages_pb2.Table(
                id=str(table.object.id),
                schema=table.object.schema_name,
                table=table.object.name
            ) for table in list(deserialize('json', tables))
        ]
        response = stub.GetColumns(storages_pb2.ColumnRequest(
            vendor=vendor,
            uri=uri,
            tables=table_list,
        ))

        if response.success:
            print(response)


def run_get_views(vendor, uri, schema, table, row, columns=None):
    with grpc.insecure_channel(GRPC_SERVER_URL) as channel:
        stub = storages_pb2_grpc.DataSourceManageServiceStub(channel)
        response = stub.GetViews(storages_pb2.ViewRequest(
            vendor=vendor,
            uri=uri,
            schema=schema,
            table=table,
            row=row,
            columns=columns
        ))

        if response.success:
            data = pickle.loads(response.records)
            return data


def run_do_migration(source_uri, destination_uri, table):
    with grpc.insecure_channel(GRPC_SERVER_URL) as channel:
        stub = storages_pb2_grpc.DataSourceManageServiceStub(channel)
        response = stub.DoMigration(storages_pb2.MigrationRequest(
            source_uri=source_uri,
            destination_uri=destination_uri,
            table=table
        ))

        if response.success:
            return response.message
