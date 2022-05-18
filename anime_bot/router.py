from rest_framework import routers

from anime_bot.views import AnimeViewSet, GenresViewSet

router = routers.DefaultRouter()
router.register(r'animebase', AnimeViewSet)
router.register(r'genres', GenresViewSet)