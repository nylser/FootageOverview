from django.core.management.base import BaseCommand, CommandError
from FootageManager.models import Camera


class Command(BaseCommand):
    help = 'Runs a scan for new footage on all cameras and adds them to the database'

    def handle(self, *args, **options):
        for c in Camera.objects.all():
            added = c.do_scan()
            self.stdout.write(self.style.SUCCESS(c.name+' added ' + str(added) + ' elements.'))
