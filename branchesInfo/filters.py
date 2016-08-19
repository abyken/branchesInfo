import django_filters
from .models import Branch

class BranchFilter(django_filters.FilterSet):

	class Meta:
		model = Branch

	isActive = django_filters.MethodFilter()
	isCashIn = django_filters.MethodFilter()
	isAroundTheClock = django_filters.MethodFilter()
	type = django_filters.MethodFilter()
	currencies = django_filters.MethodFilter()
	branchNumber = django_filters.MethodFilter()
	city = django_filters.MethodFilter()
	name = django_filters.MethodFilter()
	address = django_filters.MethodFilter()
	services = django_filters.MethodFilter()
	clients = django_filters.MethodFilter()

	def filter_isActive(self, queryset, value):
		return queryset.filter(isActive=value)

	def filter_isCashIn(self, queryset, value):
		return queryset.filter(isCashIn=value)

	def filter_isAroundTheClock(self, queryset, value):
		print value
		return queryset.filter(isAroundTheClock=value)

	def filter_type(self, queryset, value):
		return queryset.filter(type=value)

	def filter_currencies(self, queryset, value):
		return queryset.filter(currencies__in=[value])

	def filter_branchNumber(self, queryset, value):
		return queryset.filter(branchNumber__icontains=value)

	def filter_city(self, queryset, value):
		return queryset.filter(city__icontains=value)

	def filter_name(self, queryset, value):
		return queryset.filter(name__icontains=value)

	def filter_address(self, queryset, value):
		return queryset.filter(address__icontains=value)

	def filter_services(self, queryset, value):
		return queryset.filter(services__in=[value])

	def filter_clients(self, queryset, value):
		return queryset.filter(clients=value)


