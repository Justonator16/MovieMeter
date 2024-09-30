from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    path('movies/<str:movie_title>/reviews/', views.paginated_reviews_list, name='paginated_reviews'),
    path('movies/<str:movie_title>/reviews/<int:review_id>/', views.paginated_reviews_list, name='review_detail'),
]