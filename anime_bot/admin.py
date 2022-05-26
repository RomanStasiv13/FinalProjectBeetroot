from django.contrib import admin
from anime_bot.models import Anime, Genres, Studio, Subscriber

# Register your models here.

admin.site.register(Anime)
admin.site.register(Genres)
admin.site.register(Studio)
admin.site.register(Subscriber)

