
import requests
from django.core.management.base import BaseCommand
from anime_bot.models import Genres

class Command(BaseCommand):

    def handle(self, *args, **options):
        r = requests.get('https://api.jikan.moe/v4/genres/anime')
        data = r.json()
        uniq_genres = list({v['mal_id']: v for v in data['data']}.values())
        for field in uniq_genres:
            genre, _ = Genres.objects.update_or_create(id_g=field['mal_id'],
                                                       title=field['name'])

