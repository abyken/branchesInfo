import json
from django.contrib import admin
from .models import *
from .serializers import *
from django.http import HttpResponse

@admin.register(Break)
class BreakAdmmin(admin.ModelAdmin):
	pass


@admin.register(Currency)
class CurrencyAdmmin(admin.ModelAdmin):
	pass


@admin.register(Service)
class ServiceAdmmin(admin.ModelAdmin):
	pass

@admin.register(Day)
class DayAdmmin(admin.ModelAdmin):
	pass

@admin.register(Schedule)
class ScheduleAdmmin(admin.ModelAdmin):
	pass

def download_json(modeladmin, request, queryset):
	serializer = BranchInfoSerializer(queryset, many=True)

	response = HttpResponse(json.dumps(serializer.data), content_type='application/json')
	response['Content-Disposition'] = 'attachment; filename="branches.json"'

	return response

download_json.short_description = u"Download JSON of selected Branches"

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
	actions = [download_json]
