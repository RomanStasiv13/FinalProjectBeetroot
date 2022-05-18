from django.db import models


# Create your models here.


class Anime(models.Model):
    id_a = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    url_img = models.CharField(max_length=255)
    year = models.IntegerField(blank=True, null=True)
    score = models.FloatField()
    id_s = models.ForeignKey('Studio', on_delete=models.PROTECT, default=None)
    genres = models.ManyToManyField('Genres', blank=True, related_name='animes')
    episodes = models.IntegerField(blank=True, null=True)
    rating = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)

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


class Trailer(models.Model):
    id_t = models.AutoField(primary_key=True)
    url = models.CharField(max_length=255)
