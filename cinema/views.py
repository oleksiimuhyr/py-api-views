from rest_framework import status, generics, mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from cinema.models import Genre, Actor, CinemaHall, Movie
from cinema.serializers import (GenreSerializer, ActorSerializer,
                                CinemaHallSerializer, MovieSerializer)


class GenreList(APIView):
    def get(self: Genre, request: Request) -> Response:
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self: Genre, request: Request) -> Response:
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenreDetail(APIView):
    def get_object(self: Genre, pk: int) -> Genre:
        return get_object_or_404(Genre, pk=pk)

    def get(self: Genre, request: Request, pk: int) -> Response:
        serializer = GenreSerializer(self.get_object(pk=pk))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self: Genre, request: Request, pk: int) -> Response:
        serializer = GenreSerializer(
            self.get_object(pk=pk),
            data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        instance = self.get_object(pk=pk)
        serializer = GenreSerializer(
            instance,
            data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self: Genre, request: Request, pk: int) -> Response:
        self.get_object(pk=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActorList(generics.GenericAPIView,
                mixins.ListModelMixin,
                mixins.CreateModelMixin):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    def get(self: Actor, request: Request, *args, **kwargs) -> Response:
        return self.list(request, *args, **kwargs)

    def post(self: Actor, request: Request, *args, **kwargs) -> Response:
        return self.create(request, *args, **kwargs)


class ActorDetail(generics.GenericAPIView,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    def get(self: Actor, request: Request, *args, **kwargs) -> Response:
        return self.retrieve(request, *args, **kwargs)

    def put(self: Actor, request: Request, *args, **kwargs) -> Response:
        return self.update(request, *args, **kwargs)

    def delete(self: Actor, request: Request, *args, **kwargs) -> Response:
        return self.destroy(request, *args, **kwargs)

    def patch(self: Actor, request: Request, *args, **kwargs) -> Response:
        return self.partial_update(request, *args, **kwargs)


class CinemaHallViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
