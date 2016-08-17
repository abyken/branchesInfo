import os
import json
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.contrib.auth.models import User
from django.conf import settings 

class Command(BaseCommand):

	help = (
		 u'Load branch data from app/fixtures/branches.json file'
	)


	def handle(self, *args, **options):
		data_string = ""

		with open(os.path.join(settings.BASE_DIR, 'branchesInfo/fixture/branches.json'), 'r') as json_file:
			data_string=json_file.read().replace('\n', '')

		data = json.loads(data_string)

		print data