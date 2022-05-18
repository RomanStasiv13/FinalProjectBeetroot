from django.urls import path, include
from anime_bot import views

urlpatterns = [
    path('api/animebase/', views.animebase, name='animebase'),
    # path('api/animebase/<int:pk>', views.animebase, name='api_anime_base'),
]
