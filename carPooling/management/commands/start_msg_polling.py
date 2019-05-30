import multiprocessing
from django.core.management.base import BaseCommand
from django.core.cache import cache
from carPooling import msg_polling

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        p = multiprocessing.Process(target=msg_polling.runserver_from_start)
        p.start()
        self.stdout.write('msg_polling start\n')