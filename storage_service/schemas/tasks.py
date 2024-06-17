from celery import shared_task
from grpc_client.client import run_get_tables

@shared_task
def get_tables_task(vendor, uri, schemas):
    run_get_tables(vendor, uri, schemas)
