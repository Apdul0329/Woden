from rest_framework import routers

from columns.views import ColumnViewSet

app_name = 'columns'

router = routers.DefaultRouter()
router.register('', ColumnViewSet)

urlpatterns = router.urls