from rest_framework import viewsets, response, filters, status
from rest_framework.decorators import list_route, detail_route
from .models import *
from .serializers import *
from .filters import *

class BranchViewSet(viewsets.ModelViewSet):
	queryset = Branch.objects.all()
	serializer_class = BranchSerializer

	def get_queryset(self):
		queryset = super(self.__class__, self).get_queryset()
		filtered_qs = BranchFilter(self.request.query_params, queryset)

		return filtered_qs.qs

	
class BreakViewSet(viewsets.ModelViewSet):
	queryset = Break.objects.all()
	serializer_class = BreakSerializer

	
class CurrencyViewSet(viewsets.ModelViewSet):
	queryset = Currency.objects.all()
	serializer_class = CurrencySerializer

	
class ServiceViewSet(viewsets.ModelViewSet):
	queryset = Service.objects.all()
	serializer_class = ServiceSerializer

	
class ScheduleViewSet(viewsets.ModelViewSet):
	queryset = Schedule.objects.all()
	serializer_class = ScheduleSerializer

class InitialStateViewSet(viewsets.ViewSet):

	def list(self, request):
		currency_qs = Currency.objects.all()
		service_qs = Service.objects.all()

		currency_ser = CurrencySerializer(currency_qs, many=True)
		service_ser = ServiceSerializer(service_qs, many=True)

		return response.Response({"currencies": currency_ser.data, "services": service_ser.data}, status=status.HTTP_200_OK)

class BranchesInfoViewSet(viewsets.ModelViewSet):
	queryset = Branch.objects.all()
	serializer_class = BranchInfoSerializer


	
