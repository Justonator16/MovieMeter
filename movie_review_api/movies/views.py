from django.shortcuts import render
from .omdb_api import MovieInfoToJson, get_movie_detail
from .forms import MovieForm
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from rest_framework.generics import ListAPIView
from .serializers import ReviewSerializer
from .models import Review
    
def home(request):
    if request.method == 'POST':
        movies = MovieInfoToJson(movie_title=request.POST['movie_title'])
        context = {'movies': movies}

        return render(request, 'search_results.html', context=context)
    else:
        # By default the page is suppose to show new movies of the current year in order of release
        movies = MovieInfoToJson("Avengers")
        form = MovieForm()
        context = {'form': form, 'movies': movies }
        return render(request, 'home.html' , context=context)

def movie_details(request, movie_title):
    movie_json = get_movie_detail(movie_title)
        
    context = {'movie': movie_json}
    return render(request, 'movie_detail.html', context)

@login_required()
def movie_review(request, movie_title):
    return render(request, 'movie_review.html')

class MovieReviewListAPIView(ListAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    

    
        

    


