import random
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.contrib.auth.models import User

class Command(BaseCommand):

    help = (
         u'Create admin with all exist permissions.'
    )


    def handle(self, *args, **options):
        user = User.objects._create_user('admin', 'abyken.nurlan@gmail.com', 'password', True, True)