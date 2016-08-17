#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.conf import settings 
from branchesInfo.models import *
from django.db import transaction


class Command(BaseCommand):

	help = (
		 u'Load branch data from app/fixtures/branches.json file'
	)

	@transaction.atomic
	def handle(self, *args, **options):
		print "STARTED"
		data_string = ""

		with open(os.path.join(settings.BASE_DIR, 'branchesInfo/fixtures/branches.json'), 'r') as json_file:
			data_string=json_file.read().replace('\n', '')

		data = json.loads(data_string)

		def parse_schedule(branch, value):
			if value.lower() == u"круглосуточно":
				branch.isAroundTheClock = True
			elif value.lower() == u"пропускная система":
				branch.isLimitedAccess = True
			else:
				all_days_list = list(Day.objects.all().order_by('date_created'))
				scheduleWD = branch.schedule.get(type=Schedule.WD)	
				scheduleWD.days.clear()
				scheduleSD = branch.schedule.get(type=Schedule.SD)	
				scheduleSD.days.clear()

				parts = value.split(";")
				if len(parts) == 1:
					time_parts = value.split("-")
					scheduleWD.time_from = time_parts[0]
					scheduleWD.time_to = time_parts[1]
					scheduleWD.days.add(*all_days_list)
				elif len(parts) > 1:
					wd = parts[0].lower()[:5]
					time_parts = parts[0][6:].split("-")
					scheduleWD.time_from = time_parts[0]
					scheduleWD.time_to = time_parts[1]
					if wd == u"пн-пт":
						scheduleWD.days.add(*all_days_list[:5])
						if u"вых" not in parts[1].lower():
							sd_parts = parts[1].lower().split(":")
							time_parts = ":".join(sd_parts[1:]).split("-")
							scheduleSD.time_from = time_parts[0]
							scheduleSD.time_to = time_parts[1]
							if u"сб" in sd_parts[0]:
								scheduleSD.days.add(all_days_list[5])
							if u"вс" in sd_parts[0]:
								scheduleSD.days.add(all_days_list[6])

					elif wd == u"пн-сб":
						scheduleWD.days.add(*all_days_list[:6])
					elif wd == u"пн-вс":
						scheduleWD.days.add(*all_days_list)

				scheduleWD.save()
				scheduleSD.save()

		def parse_services(branch, value):
			
			def get_or_create_service(value):
				service, created = Service.objects.get_or_create(name=service_name)

				if created:
					service.save()

				return service

			if value[-1] == u".":
				value = value[:-1]		

			service_names = value.split(",")
			for service_name in service_names:
				if u"Кредиты" in service_name:
					parts = service_name.split(":")
					types = parts[1].split(u"и")

					for _type in types:
						branch.services.add(get_or_create_service(u"Кредиты " + _type.strip()))

				elif u"Переводы" in service_name:
					parts = service_name.split(":")
					types = parts[1].split(u"/")

					for _type in types:
						branch.services.add(get_or_create_service(u"Переводы " + _type.strip()))
						
				else:
					branch.services.add(get_or_create_service(service_name))

		cnt = 0
		for item in data:
			branch = Branch(
								isActive=item.get("isActive", True),
								isCashIn=item.get("cashIn", False),
								lat=item["location"]["lat"],
								lng=item["location"]["lng"],
								branchNumber=item["address"]["postalCode"],
								city=item["address"]["city"],
								address=item["address"]["streetAddress"]
							)
			branch.branchBreak = Break.create_default()
			branch.save()
			branch.create_default_schedule()

			for info in item["info"]["ru"]["notes"]:
				if info["name"] == u"Режим работы:":
					parse_schedule(branch, info["value"])

				if info["name"] == u"Перерыв:":
					branchBreak = branch.branchBreak
					if info["value"].lower() == u"без перерыва" or info["value"].lower() == u"нет":
						branchBreak.isWithoutBreak = True
					elif info["value"].lower() == u"по скользящему графику":
						branchBreak.isFlexible = True
					else:
						parts = info["value"].split("-")
						branchBreak.time_from = parts[0]
						branchBreak.time_to = parts[1]
					branchBreak.save()

				if info["name"] == u"Доступ:":
					if info["value"].lower() == u"ограниченный":
						branch.access = Branch.LIMITED
					else:
						branch.access = Branch.UNLIMITED

				if info["name"] == u"Услуги:":
					parse_services(branch, info["value"])

				if info["name"] == u"Клиенты:":
					if info["value"].lower() == u"физ. лица":
						branch.clients = Branch.INDIVIDUAL
					elif info["value"].lower() == u"юр. лица":
						branch.clients = Branch.CORPORATION	
					elif info["value"].lower() == u"физ. лица/юр. лица":
						branch.clients = Branch.BOTH

			if item.get("type", "branch") == "atm24":
				branch.type = Branch.ATM
				branch.isAroundTheClock = True
			else:
				branch.type = item.get("type")

			branch.currencies.add(Currency.objects.get(code="KZT"))
			branch.save()
			cnt += 1

			print cnt, branch.branchNumber, "CREATED"

		print "FINISHED! CREATED %s BRANCHES!"%cnt


