from rest_framework import serializers

from anime_bot.models import Anime, Genres, Studio, Subscriber


class AnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anime
        fields = [
            "id_a",
            "title",
            "title_eng",
            "title_jap",
            "description",
            "url_img",
            "year",
            "score",
            "episodes",
            "rating",
            "status",
            "trailer_url",
            "id_s",
            "genres",
            "demographics_genres",
            "themes",
            "explicit_genres",
        ]


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ['id_g', 'title', ]


class StudiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = ['id_s', 'title', ]


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = '__all__'
