#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# Create your models here.

class BaseModel(models.Model):
	date_created = models.DateTimeField(auto_now_add=True)
	date_edited = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class Break(BaseModel):
	time_from = models.CharField(max_length=50, null=True, blank=True)
	time_to = models.CharField(max_length=50, null=True, blank=True)
	isFlexible = models.BooleanField(default=False)
	isWithoutBreak = models.BooleanField(default=False)

	def __unicode__(self):
		if self.isWithoutBreak:
			return "without break"

		return self.time_from + "-" + self.time_to

	@classmethod
	def create_default(cls):
		branchBreak = Break(time_from="13:00",
								  time_to="14:00",
								  isWithoutBreak=False)
		branchBreak.save()
		return branchBreak


class Currency(BaseModel):
	code = models.CharField(max_length=10)
	description = models.CharField(max_length=255)

	class Meta:
		verbose_name_plural="Currencies"

	def __unicode__(self):
		return self.code


class Service(BaseModel):
	name = models.CharField(max_length=255)

	def __unicode__(self):
		return self.name


class Day(BaseModel):
	DAY_KEYS = (MON, TUE, WED, THU, FRI, SAT, SUN) = ("MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN")
	DAY_CAPS = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
	DAY_OPTIONS = zip(DAY_KEYS, DAY_CAPS)

	name = models.CharField(max_length=10, choices=DAY_OPTIONS, unique=True)

	def __unicode__(self):
		return self.get_name_display();

	@classmethod
	def get_day_short(cls, name):
		days_short = {
					"MON": u"пн",
					"TUE": u"вт",
					"WED": u"ср",
					"THU": u"чт",
					"FRI": u"пт",
					"SAT": u"сб",
					"SUN": u"вс"
				}

		return days_short[name]




class Schedule(BaseModel):
	TYPE_KEYS = (WD, SD) = ('WD', 'SD')
	TYPE_CAPS = ('Working day', 'Short day')
	TYPE_OPTIONS = zip(TYPE_KEYS, TYPE_CAPS)

	type = models.CharField(max_length=2, choices=TYPE_OPTIONS, default=WD)
	days = models.ManyToManyField(Day, related_name="schedule", blank=True)
	time_from = models.CharField(max_length=50, null=True, blank=True)
	time_to = models.CharField(max_length=50, null=True, blank=True)

	def get_days(self):
		return [day.name for day in self.days.all()]

	def get_type_verbose(self):
		return u'Рабочие дни' if self.type == Schedule.WD else u'Короткие дни'

	@classmethod
	def get_days_interval_string(cls, days):
		if len(days) == 1:
			return Day.get_day_short(days[0].name)

		day_start = u""
		day_end = u""

		for day in Day.objects.all().order_by("date_created"):
			if day in days:
				if not day_start:
					day_start = Day.get_day_short(day.name)

				day_end = Day.get_day_short(day.name)

		return day_start + u"-" + day_end


class BranchManager(models.Manager):

	def create_branch(self, **data):
		

		data['branchBreak'] = Break.create_default()

		branch = Branch.objects.create(**data)
		branch.create_default_schedule()	
		return branch

	def update_branch(self, instance, **data):
		branchBreak = data.pop('branchBreak', dir(instance.branchBreak))
		services = data.pop('services', [])
		currencies = data.pop('currencies', [])
		schedules = data.pop('schedule', [])

		branchBreakObject = Break.objects.get(id=branchBreak.get('id', instance.branchBreak.id))
		branchBreakObject.isWithoutBreak = branchBreak.get('isWithoutBreak', instance.branchBreak.isWithoutBreak)
		branchBreakObject.time_from = None if branchBreakObject.isWithoutBreak else branchBreak.get('time_from', instance.branchBreak.time_from)
		branchBreakObject.time_to = None if branchBreakObject.isWithoutBreak else  branchBreak.get('time_to', instance.branchBreak.time_to)

		branchBreakObject.save()
		
		data['branchBreak'] = branchBreakObject

		for k, v in data.iteritems():
			setattr(instance, k, v)

		instance.isEmpty = False
		instance.save()

		instance.services.clear()
		for service in services:
			instance.services.add(service)

		instance.currencies.clear()
		for currency in currencies:
			instance.currencies.add(currency)

		for schedule in schedules:
			scheduleObj = Schedule.objects.get(id=schedule.get('id'))
			scheduleObj.days.clear()
			scheduleObj.time_from = schedule.get('time_from', scheduleObj.time_from)
			scheduleObj.time_to = schedule.get('time_to', scheduleObj.time_to)
			scheduleObj.save()

			for day in schedule.get('get_days', []):
				dayObj = Day.objects.get(name=day)
				scheduleObj.days.add(dayObj)

		
		return instance


class Branch(BaseModel):
	TYPE_KEYS = (BRANCH, ATM, TEMINAL) = ('branch', 'atm', 'kiosk')
	TYPE_CAPS = (u'Отделение', u'Банкомат', u'Терминал')
	TYPE_OPTIONS = zip(TYPE_KEYS, TYPE_CAPS)

	CLIENT_KEYS = (INDIVIDUAL, CORPORATION, BOTH) = ('INDIVIDUAL', 'CORPORATION', 'BOTH')
	CLIENT_CAPS = (u'Физ. лица', u'Юр. лица', u'Физ. лица/Юр. лица"')
	CLIENT_OPTIONS = zip(CLIENT_KEYS, CLIENT_CAPS)

	ACCESS_KEYS = (LIMITED, UNLIMITED) = ('LIMITED', 'UNLIMITED')
	ACCESS_CAPS = (u'Ограниченный', u'Неограниченный')
	ACCESS_OPTIONS = zip(ACCESS_KEYS, ACCESS_CAPS)


	isActive = models.BooleanField(default=True)
	type = models.CharField(max_length=10, choices=TYPE_OPTIONS, default=BRANCH)
	isCashIn = models.BooleanField(default=False)
	isEmpty = models.BooleanField(default=True)
	isLimitedAccess = models.BooleanField(default=False)
	isAroundTheClock = models.BooleanField(default=False)
	lat = models.DecimalField(max_digits=15, decimal_places=6, null=True, blank=True)
	lng = models.DecimalField(max_digits=15, decimal_places=6, null=True, blank=True)
	branchNumber = models.IntegerField(null=True, blank=True)
	city = models.CharField(max_length=1024, null=True, blank=True)
	name = models.CharField(max_length=1024, null=True, blank=True)
	address = models.CharField(max_length=1024, null=True, blank=True)
	clients = models.CharField(max_length=10, choices=CLIENT_OPTIONS, default=INDIVIDUAL)
	access = models.CharField(max_length=10, choices=ACCESS_OPTIONS, default=UNLIMITED)
	branchBreak = models.ForeignKey(Break, related_name="branches", blank=True, on_delete=models.CASCADE)
	currencies = models.ManyToManyField(Currency, related_name="branches", blank=True)
	services = models.ManyToManyField(Service, related_name="branches", blank=True)
	schedule = models.ManyToManyField(Schedule, related_name="branches", blank=True)

	objects = BranchManager()

	class Meta:
		verbose_name_plural="Branches"

	def __unicode__(self):
		number = "#" + str(self.branchNumber) if self.branchNumber else u""

		return self.get_type_cap() + u" " + number

	def get_service_ids(self):
		return [service.id for service in self.services.all()]

	def get_currency_ids(self):
		return [currency.id for currency in self.currencies.all()]

	def get_type(self):
		if self.type == Branch.ATM and self.isAroundTheClock:
			return u'atm24'

		return self.type

	def get_type_cap(self):
		if self.type == Branch.ATM and self.isAroundTheClock:
			return u"Банкомат 24"

		return self.get_type_display()

	def get_location(self):
		return {
					'lat': self.lat,
					'lng': self.lng
				}

	def get_address(self):
		return {
					"postalCode": self.branchNumber,
					"city": self.city,
					"country": u"KZ",
					"streetAdress": self.address
				}

	def get_info(self):
		return {
					"ru": {
								"title": self.get_type_cap(),
								"notes": self.get_notes()
						  }
				}

	def get_notes(self):
		data = []
		excludes = ('id', 'type', 'isCashIn', 'isEmpty', 'isActive', 'lat', 'lng', 'branchNumber', 'date_created', 'date_edited', 'schedule')
		for field_name in self._meta.get_all_field_names():
			value = getattr(self, field_name)

			if field_name in excludes or not value:
				continue

			if field_name == 'address':
				data.append({'name': u'Адрес', 'value': value})

			elif field_name == "currencies" and self.type != Branch.BRANCH:
				data.append({'name': u'Валюты', 'value': ", ".join([currency.code for currency in self.currencies.all()]) })

			elif field_name == "branchBreak_id":
				data.append({'name': u'Перерыв', 'value': u'Без перерыва' if self.branchBreak.isWithoutBreak else self.branchBreak.__unicode__() })

			elif field_name == 'access' and self.type != Branch.BRANCH:
				data.append({'name': u'Доступ', 'value': self.get_access_display()})

			elif field_name == 'services' and self.type == Branch.BRANCH:
				data.append({'name': u'Услуги', 'value': ", ".join([service.name for service in self.services.all()])})

			elif field_name == 'clients' and self.type == Branch.BRANCH:
				data.append({'name': u'Клиенты', 'value': self.get_clients_display()})

		data.append({'name': u'Режим работы', 'value': self.get_schedule_unicode()})

		return data

	def get_schedule_unicode(self):
		if self.isAroundTheClock:
			return u'Круглосуточно'

		unicode_string = []
		string_parts = u""
		working_days = []

		for schedule in self.schedule.all():
			if not schedule.days.count():
				continue

			days = list(schedule.days.all())
			days_interval = Schedule.get_days_interval_string(days)
			working_days.extend(days)

			time = schedule.time_from + u"-" + schedule.time_to
			string_parts += days_interval + ": "
			string_parts += time
			unicode_string.append(string_parts)
			string_parts = u""

		days_off = list(set(Day.objects.all()) - set(working_days))

		if days_off:
			days_interval = Schedule.get_days_interval_string(days_off)
			string_parts = days_interval + u": выходной"
			unicode_string.append(string_parts)

		return "; ".join(unicode_string)

	def create_default_schedule(self):
		scheduleWD = Schedule(type=Schedule.WD,
									time_from="09:00",
									time_to="18:00")
		scheduleSD = Schedule(type=Schedule.SD,
									time_from=None,
									time_to=None)
		scheduleWD.save()
		scheduleSD.save()

		for day in Day.objects.all():
			if day.name not in [Day.SAT, Day.SUN]:
				scheduleWD.days.add(day)
		
		self.schedule.add(scheduleWD, scheduleSD)



