import json

from django.db.models import Prefetch
from rest_framework import generics, status
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from consigliflix.models import Movie, MoviesSeen, Review
from consigliflix.serializers import MovieSerializer, RegisterSerializer, TokenSerializer, AuthenticatedMovieSerializer, \
    ReviewSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class TokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = TokenSerializer


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_all_movie(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    if request.user.is_authenticated:
        movies = Movie.objects.prefetch_related(
            Prefetch('watchers', queryset=MoviesSeen.objects.filter(user_id=request.user.id)))

        serializer = AuthenticatedMovieSerializer(movies, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_movie(request, pk, format=None):
    try:
        movie = Movie.objects.prefetch_related(
            Prefetch('watchers', queryset=MoviesSeen.objects.filter(user_id=request.user.id))
        ).get(pk=pk)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MovieSerializer(movie, many=False)
        return Response(serializer.data)
    elif request.method == 'POST':
        if movie.watchers == 0:
            movie.watchers.create(user_id=request.user.id)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_409_CONFLICT)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def already_seen_movies(request):
    movies = Movie.objects.filter(watchers__user_id=request.user.id)
    serializer = AuthenticatedMovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def filter_by_platform(request, platform):
    movies = Movie.objects.filter(availability__platform__name__icontains=platform)
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def review(request, movie):
    if request.method == 'GET':
        movie_reviews = Review.objects.prefetch_related('movie').prefetch_related('user').filter(movie=movie)
        serializer = ReviewSerializer(movie_reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        Review.objects.create(movie=Movie.objects.get(pk=movie),
                              user=User.objects.get(username=body['username']),
                              rate=body['rate'],
                              review=body['review'])
        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def filter_reviews_by_user(request, username):
    user = User.objects.get(username=username)
    movie_reviews = Review.objects.prefetch_related('movie').prefetch_related('user').filter(user=user)
    serializer = ReviewSerializer(movie_reviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def filter_reviews_by_movie(request, movie_name):
    movie = Movie.objects.filter(title__icontains=movie_name)
    movie_reviews = Review.objects.prefetch_related('movie').prefetch_related('user').filter(movie=movie)
    serializer = ReviewSerializer(movie_reviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_not_seen_movie(request):
    movies = Movie.objects.prefetch_related('watchers').filter(watchers__isnull=True)
    serializer = AuthenticatedMovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
