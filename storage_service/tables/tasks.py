from celery import shared_task
from grpc_client.client import run_get_columns

@shared_task
def get_columns_task(vendor, uri, tables):
    run_get_columns(vendor, uri, tables)