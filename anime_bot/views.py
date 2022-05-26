from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from anime_bot.models import Anime, Genres, Studio, Subscriber
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.
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
    filterset_fields = ['chat_id', 'status']

# class SubscriberList(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """
#     def get(self, request, format=None):
#         subscriber = Subscriber.objects.all()
#         serializer = SubscriberSerializer(subscriber, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = SubscriberSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class SubscriberDetail(APIView):
#     """
#     Retrieve, update or delete a snippet instance.
#     """
#     def get_object(self, pk):
#         try:
#             return Subscriber.objects.get(pk=pk)
#         except Subscriber.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SubscriberSerializer(snippet)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SubscriberSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)