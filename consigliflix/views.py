from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from consigliflix.models import Movie
from consigliflix.serializers import MovieSerializer, RegisterSerializer, TokenSerializer


class MovieSet(ModelViewSet):
    queryset = Movie.objects.all().order_by('title')
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class TokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = TokenSerializer

