from rest_framework import routers

from storages.views import StorageViewSet

app_name = 'storages'

router = routers.DefaultRouter()
router.register('', StorageViewSet)

urlpatterns = router.urls