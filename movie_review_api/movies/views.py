from django.urls import reverse_lazy 
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .omdb_api import MovieInfoToJson, get_movie_detail, filter_search_results, get_popular_movies
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from .models import Review
from django.contrib import messages
from django.core.paginator import Paginator   
import random

def landing_page(request):
    message.success(request, f"Welcome {request.user}")
    return render(request, 'landing_page.html')

def home(request):
    if request.method == 'POST':
        try:
            movies = MovieInfoToJson(movie_title=request.POST.get('movie_title'))
        except:
            return redirect(reverse_lazy('movies:home'))
        
        #Eg Imdb Ratings, Director, plot, runtime etc
        movies_full_details = [ get_movie_detail(movie['Title']) for movie in movies ]
        
        filter_by = request.POST.get('filter') 
        if filter_by != None:
            filtered_movies = filter_search_results(movies_full_details , filter_by)
            context = {'movies': filtered_movies}
            return render(request, 'search_results.html', context=context)

        #Unfiltered movies from api
        context = {'movies': movies_full_details}
                        
        return render(request, 'search_results.html', context=context)
    else:
        # Popular 30 movies
        movies = get_popular_movies(50)
        
        try:
            popular_movies_full_details = [ get_movie_detail(movie['title']) for movie in movies ]
        except:
            popular_movies_full_details = [ get_movie_detail(movie['Title']) for movie in movies ]
        
        # Paginate results (e.g., 30 reviews per page)
        paginator = Paginator(popular_movies_full_details, 25)  # Show 30 reviews per page
        page_number = random.randint(1,2)
        page_objs = paginator.get_page(page_number)

        context = {'movies': page_objs }
        return render(request, 'home.html' , context=context)

def movie_details(request, movie_title):
    movie_json = get_movie_detail(movie_title)
    #All reviews with title from request
    movies = Review.objects.filter(movie_title=movie_title)
    sum_of_rating = 0
    #Some movies are not rated under MovieMeter and might return a ZeroDivision Error
    try: 
        for movie in movies:
            sum_of_rating += movie.rating
        
        average_rating = sum_of_rating / len(movies)
    except:
        average_rating = 'Not rated'
    
    context = {'movie': movie_json, 'average_rating': average_rating }
    return render(request, 'movie_detail.html', context)

#Only authenticated users should be able to submit a review
@login_required(login_url=reverse_lazy('accounts:login'))
def movie_review(request, movie_title):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            # Set the reviewer and movie_title fields manually
            review.reviewer = request.user
            review.movie_title = movie_title
            # Save the review to the database
            review.save()
            
            messages.success(request, "Review added successfully ")
        return redirect(reverse_lazy('movies:home'))
    elif request.method == 'GET':
        try:
            #Check if user hasn not reviewed movie before 
            review = get_object_or_404(Review, movie_title=movie_title, reviewer=request.user)
             # Meaning user has reviewed the movie before
            if review:
                movie_json = get_movie_detail(movie_title)
                context = {'movie': movie_json}
                
                messages.error(request, "Error can not review a movie twice :(")
                return render(request, 'movie_detail.html', context)
            else:
                initial_data = {'movie_title': movie_title}
                form = ReviewForm(initial=initial_data)
                return render(request ,"movie_review.html", {'form': form})
        except Http404:
            # If the review does not exist, redirect to the rate movie page
            initial_data = {'movie_title': movie_title}
            form = ReviewForm(initial=initial_data)
            return render(request ,"movie_review.html", {'form': form, 'movie_title': movie_title})

 # All of reviews of user currently logged in
@login_required(login_url=reverse_lazy('accounts:login'))   
def user_movie_reviews(request):
    # Returns all reviews made by user logged in , in ASC order
     reviews = Review.objects.filter(reviewer=request.user.id).order_by('created_at')
     context = {'reviews': reviews}
     return render(request, 'user_reviews.html', context)
 
#CRUD ON Reviews so that a user can delete and update their own reviews
@login_required(login_url=reverse_lazy('accounts:login'))   
def update_review(request, movie_title):
    review = get_object_or_404(Review, movie_title=movie_title, reviewer=request.user.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.movie_title = movie_title
            # Save the review to the database
            review.save()
            messages.success(request, "Review successfully updated")
            return redirect(reverse_lazy('movies:my_reviews'))
    else:
        form = ReviewForm(instance=review)
        context = {'form': form, 'movie_title': movie_title}
        return render(request, 'update_review.html', context)

@login_required(login_url=reverse_lazy('accounts:login'))   
def delete_review(request, movie_title):
    if request.method == 'POST':
        review = Review.objects.filter(movie_title=movie_title, reviewer=request.user.id )
        review.delete()
        
        messages.success(request, "Review deleted successfully")
        return redirect(reverse_lazy('movies:my_reviews'))
    else:
        context = {'movie_title': movie_title}
        return render(request, 'delete_review.html', context)

@login_required(login_url=reverse_lazy('accounts:login'))   
# All reviews of a specific movie by all users who reviewed the movie
def all_reviews(request, movie_title):
    reviews = Review.objects.filter(movie_title=movie_title)
    
    sort_by = request.GET.get('sort', 'created_at')
    if sort_by == 'rating':
        reviews = reviews.order_by('rating')
    elif sort_by == 'reviewer':
        reviews = reviews.order_by('reviewer_id') # Sort by Reviewer username
    else:
        reviews = reviews.order_by('-created_at')  # Default sorting by newest first
        
    # Paginate results (e.g., 5 reviews per page)
    paginator = Paginator(reviews, 5)  # Show 5 reviews per page
    page_number = request.GET.get('page')
    page_reviews = paginator.get_page(page_number)
        
    context = {
        'reviews': reviews, 
        'movie_title': movie_title,
        'sort_by': sort_by}
    return render(request, 'all_reviews.html', context)