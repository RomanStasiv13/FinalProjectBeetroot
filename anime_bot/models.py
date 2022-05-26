from datetime import datetime
from django.db import models


# Create your models here.


class Anime(models.Model):
    id_a = models.AutoField(primary_key=True)

    title = models.CharField(max_length=255)
    title_eng = models.CharField(max_length=255, blank=True, null=True)
    title_jap = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url_img = models.URLField(blank=True, null=True, default=None)
    year = models.IntegerField(blank=True, null=True)
    score = models.FloatField(blank=True, null=True)
    id_s = models.ForeignKey('Studio', on_delete=models.PROTECT, default=None)
    genres = models.ManyToManyField('Genres', blank=True, related_name='animes')
    demographics_genres = models.ManyToManyField('Genres', blank=True, related_name='animes_demoghraph')
    themes = models.ManyToManyField('Genres', blank=True, related_name='animes_theme')
    explicit_genres = models.ManyToManyField('Genres', blank=True, related_name='animes_explicit')
    episodes = models.IntegerField(blank=True, null=True)
    rating = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    trailer_url = models.URLField(blank=True, null=True, default=None)
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title


class Genres(models.Model):
    id_g = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Studio(models.Model):
    id_s = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Subscriber(models.Model):
    id_u = models.AutoField(primary_key=True)
    chat_id = models.CharField(max_length=150,blank=True,null=True)
    status = models.CharField(max_length=255,blank=True,null=True)
    anime_id = models.IntegerField(blank=True,null=True)
