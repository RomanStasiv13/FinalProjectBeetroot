from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets

from anime_bot.models import Anime, Genres, Studio

# Create your views here.
from anime_bot.serializer import AnimeSerializer, GenresSerializer


def animebase(request, pk=None):
    if request.method == 'GET':
        return JsonResponse(AnimeSerializer(Anime.objects.all()[:5], many=True).data, safe=False)


class AnimeViewSet(viewsets.ModelViewSet):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer

class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
