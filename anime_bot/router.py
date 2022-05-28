from rest_framework import routers

from anime_bot.views import AnimeViewSet, GenresViewSet, StudiosViewSet, SubscriberViewSet

router = routers.DefaultRouter()
router.register(r'animebase', AnimeViewSet)
router.register(r'genres', GenresViewSet)
router.register(r'studios', StudiosViewSet)
router.register(r'subscribers', SubscriberViewSet)
