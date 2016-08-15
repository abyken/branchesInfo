from rest_framework import serializers
from .models import *

__all__ = (
	'BreakSerializer',
	'CurrencySerializer',
	'ServiceSerializer',
	'DaySerializer',
	'ScheduleSerializer',
	'BranchSerializer',
	'BranchInfoSerializer'
)

class BreakSerializer(serializers.ModelSerializer):

	class Meta:
		model = Break
		exclude = ('date_created', 'date_edited')


class CurrencySerializer(serializers.ModelSerializer):

	class Meta:
		model = Currency
		exclude = ('date_created', 'date_edited')

	id = serializers.IntegerField(read_only=False)


class ServiceSerializer(serializers.ModelSerializer):

	class Meta:
		model = Service
		exclude = ('date_created', 'date_edited')

	id = serializers.IntegerField(read_only=False)


class DaySerializer(serializers.ModelSerializer):

	class Meta:
		model = Day
		exclude = ('date_created', 'date_edited')


class ScheduleSerializer(serializers.ModelSerializer):

	class Meta:
		model = Schedule
		exclude = ('date_created', 'date_edited')

	id = serializers.IntegerField(read_only=False)
	days = serializers.ListField(source="get_days", required=False)
	type_display = serializers.CharField(source="get_type_verbose", read_only=True)

class BranchSerializer(serializers.ModelSerializer):

	class Meta:
		model = Branch
		exclude = ('date_created', 'date_edited', 'isEmpty')

	branchBreak = BreakSerializer(required=False)
	currencies = CurrencySerializer(required=False, many=True)
	services = ServiceSerializer(required=False, many=True)
	schedule = ScheduleSerializer(required=False, many=True)
	service_ids = serializers.ListField(source="get_service_ids", read_only=True)
	currency_ids = serializers.ListField(source="get_currency_ids", read_only=True)

	def create(self, validated_data):
		return Branch.objects.create_branch(**validated_data)

	def update(self, instance, validated_data):
		return Branch.objects.update_branch(instance, **validated_data)


class LocationSerializer(serializers.Serializer):
	lat = serializers.DecimalField(max_digits=15, decimal_places=6)
	lng = serializers.DecimalField(max_digits=15, decimal_places=6)


class AddressSerializer(serializers.Serializer):
	postalCode = serializers.IntegerField()
	city = serializers.CharField()
	country = serializers.CharField()
	streetAdress = serializers.CharField()


class NoteSerializer(serializers.Serializer):

	name = serializers.CharField()
	value = serializers.CharField()


class RULocaleSerializer(serializers.Serializer):
	title = serializers.CharField()
	notes = NoteSerializer(many=True)


class InfoSerializer(serializers.Serializer):
	ru = RULocaleSerializer()


class BranchInfoSerializer(serializers.Serializer):
	id = serializers.IntegerField(read_only=True)
	isActive = serializers.BooleanField(read_only=True)
	type = serializers.CharField(source="get_type", read_only=True)
	cashIn = serializers.BooleanField(source="isCashIn", read_only=True)
	location = LocationSerializer(source='get_location', read_only=True)
	address = AddressSerializer(source='get_address', read_only=True)
	info = InfoSerializer(source='get_info', read_only=True)





