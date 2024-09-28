from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path("", views.home, name="home"),
    path("<str:movie_title>/", views.movie_details, name="movie_detail"),
    path("<str:movie_title>/review", views.MovieReviewListAPIView.as_view(), name="user_movie_review"),
]