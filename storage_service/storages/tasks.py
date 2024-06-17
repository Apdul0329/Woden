from celery import shared_task
from grpc_client.client import run_get_schemas

@shared_task
def get_schemas_task(id, vendor, uri):
    run_get_schemas(id, vendor, uri)