from django.shortcuts import render
from .omdb_api import MovieInfoToJson
from .forms import MovieForm
from django.views.generic import DetailView

def home(request):
    if request.method == 'POST':
        movie_title = request.POST['movie_title']

        movies = MovieInfoToJson(movie_title=movie_title)
        context = {'movies': movies}

        return render(request, 'search_results.html', context=context)
    else:
        # By default the page is suppose to show new movies of the current year in order of release
        movies = MovieInfoToJson("Avengers")
        form = MovieForm()
        context = {'form': form, 'movies': movies }
        return render(request, 'home.html' , context=context)

def movie_detail(request, movie_title):
    ...
        

    


