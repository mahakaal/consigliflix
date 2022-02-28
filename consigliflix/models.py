from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=20)
    year = models.IntegerField(default=None, null=True)

    class Meta:
        db_table = "movies"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    review = models.TextField(default=None, null=True)

    class Meta:
        db_table = 'reviews'


class MoviesSeen(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        db_table = 'movies_seen'


class StreamingPlatforms(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'streaming_platform'


class MoviePlatforms(models.Model):
    movie = models.ForeignKey(Movie, null=True, on_delete=models.SET_NULL)
    platform = models.ForeignKey(StreamingPlatforms, on_delete=models.CASCADE)

    class Meta:
        db_table = 'movie_platforms'
