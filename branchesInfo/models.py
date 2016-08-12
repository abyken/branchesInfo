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
	isWithoutBreak = models.BooleanField(default=False)

	def __unicode__(self):
		if self.isWithoutBreak:
			return "without break"

		return self.time_from + " - " + self.time_to


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


class Schedule(BaseModel):
	TYPE_KEYS = (WD, SD, DO) = ('WD', 'SD', 'DO')
	TYPE_CAPS = ('Working day', 'Short day', 'Day off')
	TYPE_OPTIONS = zip(TYPE_KEYS, TYPE_CAPS)

	type = models.CharField(max_length=2, choices=TYPE_OPTIONS, default=WD)
	days = models.ManyToManyField(Day, related_name="schedule", blank=True)
	time_from = models.CharField(max_length=50, null=True, blank=True)
	time_to = models.CharField(max_length=50, null=True, blank=True)
	isAroundTheClock = models.BooleanField(default=False)


class BranchManager(models.Manager):

	def create_branch(self, **data):
		branchBreakObject = Break(time_from="13:00",
								  time_to="14:00",
								  isWithoutBreak=False)
		branchBreakObject.save()

		data['branchBreak'] = branchBreakObject

		branch = Branch.objects.create(**data)
		scheduleDO = Schedule(type=Schedule.DO,
									time_from=None,
									time_to=None)
		scheduleWD = Schedule(type=Schedule.WD,
									time_from="09:00",
									time_to="18:00")
		scheduleSD = Schedule(type=Schedule.SD,
									time_from=None,
									time_to=None)
		scheduleWD.save()
		scheduleSD.save()
		scheduleDO.save()
		
		branch.schedule.add(scheduleDO, scheduleWD, scheduleSD)

		for day in Day.objects.all():
			if day.name == Day.SAT or day.name == Day.SUN:
				scheduleDO.days.add(day)
			else:
				scheduleWD.days.add(day)
		
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
			serviceObject = Service.objects.get(id=service.get('id'))
			instance.services.add(service)

		instance.currencies.clear()
		for currency in currencies:
			currencyObject = Currency.objects.get(id=currency.get('id'))
			instance.currencies.add(currencyObject)

		for schedule in schedules:
			scheduleObj = Schedule.objects.get(id=schedule.get('id'))
			scheduleObj.days.clear()
			scheduleObj.isAroundTheClock = schedule.get('isAroundTheClock', scheduleObj.isAroundTheClock)
			if scheduleObj.isAroundTheClock or scheduleObj.type == Schedule.DO:
				scheduleObj.time_from = None
				scheduleObj.time_to = None
			else:
				scheduleObj.time_from = schedule.get('time_from', scheduleObj.time_from)
				scheduleObj.time_to = schedule.get('time_to', scheduleObj.time_to)
			scheduleObj.save()

			for day in schedule.get('days', []):
				dayObj = Day.objects.get(name=day['name'])
				scheduleObj.days.add(dayObj)

		
		return instance


class Branch(BaseModel):
	TYPE_KEYS = (BRANCH, ATM, ATM24, TEMINAL) = ('BRANCH', 'ATM', 'ATM24', 'TERMINAL')
	TYPE_CAPS = ('Branch', 'Atm', 'Atm24', 'Terminal')
	TYPE_OPTIONS = zip(TYPE_KEYS, TYPE_CAPS)

	CLIENT_KEYS = (INDIVIDUAL, CORPORATION, BOTH) = ('INDIVIDUAL', 'CORPORATION', 'BOTH')
	CLIENT_CAPS = ('Individual', 'Corporation', 'Individual/Corporation')
	CLIENT_OPTIONS = zip(CLIENT_KEYS, CLIENT_CAPS)

	ACCESS_KEYS = (LIMITED, UNLIMITED) = ('LIMITED', 'UNLIMITED')
	ACCESS_CAPS = ('Limited entrance', 'Unlimited entance')
	ACCESS_OPTIONS = zip(ACCESS_KEYS, ACCESS_CAPS)


	isActive = models.BooleanField(default=True)
	type = models.CharField(max_length=10, choices=TYPE_OPTIONS, default=BRANCH)
	isCashIn = models.BooleanField(default=False)
	isEmpty = models.BooleanField(default=True)
	lat = models.DecimalField(max_digits=15, decimal_places=6, null=True, blank=True)
	lng = models.DecimalField(max_digits=15, decimal_places=6, null=True, blank=True)
	branchNumber = models.IntegerField(null=True, blank=True)
	city = models.CharField(max_length=1024, null=True, blank=True)
	name = models.CharField(max_length=1024, null=True, blank=True)
	address = models.CharField(max_length=1024, null=True, blank=True)
	clients = models.CharField(max_length=10, choices=CLIENT_OPTIONS, default=INDIVIDUAL)
	access = models.CharField(max_length=10, choices=ACCESS_OPTIONS, default=UNLIMITED)
	branchBreak = models.ForeignKey(Break, related_name="branches", blank=True)
	currencies = models.ManyToManyField(Currency, related_name="branches", blank=True)
	services = models.ManyToManyField(Service, related_name="branches", blank=True)
	schedule = models.ManyToManyField(Schedule, related_name="branches", blank=True)

	objects = BranchManager()

	class Meta:
		verbose_name_plural="Branches"



