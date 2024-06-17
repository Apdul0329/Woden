from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('storages/', include('storages.urls')),
    path('schemas/', include('schemas.urls')),
    path('tables/', include('tables.urls')),
    path('columns/', include('columns.urls')),
]
