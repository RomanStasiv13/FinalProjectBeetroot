from rest_framework import serializers

from anime_bot.models import Anime, Genres


class AnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anime
        fields = '__all__'


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ['id_g', 'title',]