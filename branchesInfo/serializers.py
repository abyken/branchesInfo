from rest_framework import serializers
from .models import *

__all__ = (
	'BreakSerializer',
	'CurrencySerializer',
	'ServiceSerializer',
	'DaySerializer',
	'ScheduleSerializer',
	'BranchSerializer'
)

class BreakSerializer(serializers.ModelSerializer):

	class Meta:
		model = Break
		exclude = ('date_created', 'date_edited')


class CurrencySerializer(serializers.ModelSerializer):

	class Meta:
		model = Currency
		exclude = ('date_created', 'date_edited')


class ServiceSerializer(serializers.ModelSerializer):

	class Meta:
		model = Service
		exclude = ('date_created', 'date_edited')


class DaySerializer(serializers.ModelSerializer):

	class Meta:
		model = Day
		exclude = ('date_created', 'date_edited')


class ScheduleSerializer(serializers.ModelSerializer):

	class Meta:
		model = Schedule
		exclude = ('date_created', 'date_edited')

	days = DaySerializer(required=False, many=True)

class BranchSerializer(serializers.ModelSerializer):

	class Meta:
		model = Branch
		exclude = ('date_created', 'date_edited', 'isEmpty')

	branchBreak = BreakSerializer(required=False)
	currencies = CurrencySerializer(required=False, many=True)
	services = ServiceSerializer(required=False, many=True)
	schedule = ScheduleSerializer(required=False, many=True)

	def create(self, validated_data):
		return Branch.objects.create_branch(**validated_data)

	def update(self, instance, validated_data):
		return Branch.objects.update_branch(**validated_data)
