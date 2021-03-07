from exam.models import Standard
from django.core.management.base import BaseCommand
import django

class Command(BaseCommand):
    help = 'create standard from 1 to 10'

    def handle(self, *args, **kwargs):
        try:
            stds = ["1","2","3","4","5","6","7","8","9","10"]
            for std in stds:
                if not Standard.objects.filter(class_name=std).exists():
                    Standard(class_name=std).save()
        except django.db.utils.OperationalError:
            self.stdout.write(self.style.ERROR('Error. First create the tables by makemigrations and migration command'))
