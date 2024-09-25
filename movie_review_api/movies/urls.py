from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("<str:movie_title>/", views.movie_details, name="movie_detail"),
    path("<str:movie_title>/review", views.movie_review, name="user_movie_review"),
]