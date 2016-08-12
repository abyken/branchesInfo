from django.contrib import admin
from .models import *
# Register your models here.



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


@admin.register(Branch)
class BranchAdmmin(admin.ModelAdmin):
	pass
