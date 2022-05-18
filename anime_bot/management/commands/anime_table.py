import time
from anime_bot.models import Anime, Genres, Studio
from django.core.management.base import BaseCommand
import requests




class Command(BaseCommand):

    def handle(self, *args, **options):
        r = requests.get('https://api.jikan.moe/v4/anime')
        data = r.json()
        pages_of_anime = data['pagination']['last_visible_page']
        for i in range(1, 2):
            time.sleep(2)
            r = requests.get(f'https://api.jikan.moe/v4/anime?page={i}')
            data = r.json()
            anime_per_page = data['pagination']['items']['count']
            for i in range(int(anime_per_page)):
                genre = []
                for g in range(len(data['data'][i]['genres'])):
                    genre.append(data['data'][i]['genres'][g]['mal_id'])
                anime_data_id_genres = genre
                if data['data'][i]['studios']:
                    anime_data_studio, _ = Studio.objects.get_or_create(title=data['data'][i]['studios'][0]['name'], )
                else:
                    anime_data_studio, _ = Studio.objects.get_or_create(title='None', )
                anime, _ = Anime.objects.update_or_create(id_a=data['data'][i]['mal_id'],
                                                          title=data['data'][i]['title'],
                                                          description=data['data'][i]['synopsis'],
                                                          url_img=data['data'][i]['images']['jpg']['large_image_url'],
                                                          year=data['data'][i]['aired']['prop']['from']['year'],
                                                          score=data['data'][i]['score'],
                                                          rating=data['data'][i]['rating'],
                                                          status=data['data'][i]['status'],
                                                          episodes=data['data'][i]['episodes'],
                                                          id_s= anime_data_studio,
                                                          )
                anime.genres.add(*anime_data_id_genres)






