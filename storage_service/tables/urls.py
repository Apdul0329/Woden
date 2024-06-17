from rest_framework import routers

from tables.views import TableViewSet

app_name = 'tables'

router = routers.DefaultRouter()
router.register('', TableViewSet)

urlpatterns = router.urls