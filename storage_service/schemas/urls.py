from rest_framework import routers

from schemas.views import SchemaViewSet

app_name = 'schemas'

router = routers.DefaultRouter()
router.register('', SchemaViewSet)

urlpatterns = router.urls