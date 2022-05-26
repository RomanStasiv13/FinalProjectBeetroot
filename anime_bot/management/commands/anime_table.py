import time
from anime_bot.models import Anime, Genres, Studio
from django.core.management.base import BaseCommand
import requests


class Command(BaseCommand):

    def handle(self, *args, **options):
        r = requests.get('https://api.jikan.moe/v4/anime')
        data = r.json()
        pages_of_anime = data['pagination']['last_visible_page']
        for i in range(1, pages_of_anime + 1):
            time.sleep(2)
            r = requests.get(f'https://api.jikan.moe/v4/anime?page={i}')
            data = r.json()
            anime_per_page = data['pagination']['items']['count']
            for i in range(int(anime_per_page)):

                genre = []
                for g in range(len(data['data'][i]['genres'])):
                    genre.append(data['data'][i]['genres'][g]['mal_id'])
                anime_data_id_genres = genre

                demograph_genre = []
                for g in range(len(data['data'][i]['demographics'])):
                    demograph_genre.append(data['data'][i]['demographics'][g]['mal_id'])
                anime_data_id_demograph = demograph_genre

                theme = []
                for g in range(len(data['data'][i]['themes'])):
                    theme.append(data['data'][i]['themes'][g]['mal_id'])
                anime_data_id_themes = theme

                explicit = []
                for g in range(len(data['data'][i]['explicit_genres'])):
                    explicit.append(data['data'][i]['explicit_genres'][g]['mal_id'])
                anime_data_id_explicit = explicit

                if data['data'][i]['studios']:
                    anime_data_studio, _ = Studio.objects.get_or_create(title=data['data'][i]['studios'][0]['name'], )
                else:
                    anime_data_studio, _ = Studio.objects.get_or_create(title='None', )
                anime, _ = Anime.objects.update_or_create(id_a=data['data'][i]['mal_id'],
                                                          title=data['data'][i]['title'],
                                                          title_eng=data['data'][i]['title_english'],
                                                          title_jap=data['data'][i]['title_japanese'],
                                                          description=data['data'][i]['synopsis'],
                                                          url_img=data['data'][i]['images']['jpg']['large_image_url'],
                                                          year=data['data'][i]['aired']['prop']['from']['year'],
                                                          score=data['data'][i]['score'],
                                                          rating=data['data'][i]['rating'],
                                                          status=data['data'][i]['status'],
                                                          episodes=data['data'][i]['episodes'],
                                                          id_s=anime_data_studio,
                                                          trailer_url=data['data'][i]['trailer']['url']
                                                          )
                anime.genres.add(*anime_data_id_genres)
                anime.demographics_genres.add(*anime_data_id_demograph)
                anime.themes.add(*anime_data_id_themes)
                anime.explicit_genres.add(*anime_data_id_explicit)
