from rest_framework.routers import DefaultRouter
from branchesInfo.api_views import *
from django.conf.urls import url, include

router = DefaultRouter()
router.register(r'branches', BranchViewSet, 'branches')
router.register(r'breaks', BreakViewSet, 'breaks')
router.register(r'currencies', CurrencyViewSet, 'currencies')
router.register(r'services', ServiceViewSet, 'services')
router.register(r'schedules', ScheduleViewSet, 'schedules')
router.register(r'initial-state', InitialStateViewSet, 'initial_state')

urlpatterns = [
	url(r'api/v1/', include(router.urls))
]