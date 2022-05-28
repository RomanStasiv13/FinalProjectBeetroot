from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from anime_bot.models import Anime, Genres, Studio, Subscriber

from anime_bot.serializer import AnimeSerializer, GenresSerializer, StudiosSerializer, SubscriberSerializer


class AnimeViewSet(viewsets.ModelViewSet):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer

    def get_queryset(self):
        title = self.request.query_params.get('title')
        if title:
            return Anime.objects.filter(title__icontains=title).order_by('-score')

        genres = self.request.query_params.get('genres')
        if genres:
            genre_name = Genres.objects.filter(title__icontains=genres).first()
            if genre_name:
                return Anime.objects.filter(genres=genre_name.id_g).order_by('-score')
            return Anime.objects.filter(genres=-1)

        studio = self.request.query_params.get('studio')
        if studio:
            studio_name = Studio.objects.filter(title__icontains=studio).first()
            if studio_name:
                return Anime.objects.filter(id_s=studio_name.id_s).order_by('-score')
            return Anime.objects.filter(id_s=-1)

        return Anime.objects.all()


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class StudiosViewSet(viewsets.ModelViewSet):
    queryset = Studio.objects.all()
    serializer_class = StudiosSerializer


class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['chat_id', 'status', 'anime_id']
