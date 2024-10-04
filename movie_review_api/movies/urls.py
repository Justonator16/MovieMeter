from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path("my_reviews/", views.user_movie_reviews, name="my_reviews"),
    path("my_reviews/update/<str:movie_title>/", views.update_review, name="update_review"),
    path("my_reviews/delete/<str:movie_title>/", views.delete_review, name="delete_review"),
    path("home/", views.home, name="home"),
    #Handle movie titles with special characters eg : / or a space
    path("<path:movie_title>/", views.movie_details, name="movie_detail"),
    path("<str:movie_title>/review", views.movie_review, name="movie_review"),
    path("<str:movie_title>/all_reviews", views.all_reviews, name="all_reviews"),
   
]