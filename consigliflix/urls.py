"""consigliflix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from . import views
from .views import RegisterView, TokenPairView

router = routers.DefaultRouter()
#router.register(r'movies', views.MovieSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', TokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('movies/', views.get_all_movie),
    path('movies/<int:pk>', views.get_movie),
    path('movies/seen/', views.already_seen_movies),
    path('movies/platform/<str:platform>', views.filter_by_platform, name='platform'),
    path('movies/<int:movie>/reviews/', views.review, name='movie'),
    path('movies/reviews/<str:username>', views.filter_reviews_by_user, name='username'),
    path('movies/reviews/<str:movie_name>', views.filter_reviews_by_movie, name='movie_name'),
    path('movies/not-seen/', views.get_not_seen_movie),
]
