import time
import requests
from django.core.management.base import BaseCommand
from anime_bot.models import Studio

class Command(BaseCommand):

    def handle(self, *args, **options):
        for i in range(1, 21):
            r = requests.get(f'https://api.jikan.moe/v4/producers/?page={i}')
            data = r.json()
            time.sleep(2)
            for field in data['data']:
                studio, _ = Studio.objects.update_or_create(id_s=field['mal_id'],
                                                            title=field['name'],
                                                            )








