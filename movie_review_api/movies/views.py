from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .omdb_api import MovieInfoToJson, get_movie_detail
from .forms import MovieForm
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from .models import Review
from django.contrib import messages
from django.core.paginator import Paginator   
from django.db.models import Count 

def home(request):
    if request.method == 'POST':
        movies = MovieInfoToJson(movie_title=request.POST.get('movie_title'))
        context = {'movies': movies}

        return render(request, 'search_results.html', context=context)
    else:
        # By default the page is suppose to show new movies of the current year in order of release
        movies = MovieInfoToJson("Avengers")
        context = {'movies': movies }
        return render(request, 'home.html' , context=context)

def movie_details(request, movie_title):
    movie_json = get_movie_detail(movie_title)
        
    context = {'movie': movie_json}
    return render(request, 'movie_detail.html', context)

#Only authenticated users should be able to submit a review
@login_required(login_url=reverse_lazy('accounts:login'))
def movie_review(request, movie_title):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            # Set the reviewer and movie_title fields manually
            review.user_id = request.user
            review.movie_title = movie_title
            # Save the review to the database
            review.save()
            
            messages.success(request, "Review added successfully ")
        return redirect(reverse_lazy('movies:home'))
    elif request.method == 'GET':
        try:
            #Check if user hasn not reviewed movie before 
            review = get_object_or_404(Review, movie_title=movie_title, user_id=request.user)
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
            return render(request ,"movie_review.html", {'form': form})

 # All of reviews of user currently logged in
@login_required(login_url=reverse_lazy('accounts:login'))   
def user_movie_reviews(request):
    # Returns all reviews made by user logged in , in ASC order
     reviews = Review.objects.filter(user_id=request.user.id).order_by('created_at')
     context = {'reviews': reviews}
     return render(request, 'user_reviews.html', context)
 
#CRUD ON Reviews so that a user can delete and update their own reviews
@login_required(login_url=reverse_lazy('accounts:login'))   
def update_review(request, movie_title):
    review = get_object_or_404(Review, movie_title=movie_title, user_id=request.user.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.user_id = request.user
            review.movie_title = movie_title
            # Save the review to the database
            review.save()
            messages.success(request, "Review successfully updated")
            return redirect(reverse_lazy('movies:my_reviews'))
    else:
        form = ReviewForm(instance=review)
        context = {'form': form}
        return render(request, 'update_review.html', context)

@login_required(login_url=reverse_lazy('accounts:login'))   
def delete_review(request, movie_title):
    if request.method == 'POST':
        review = Review.objects.filter(movie_title=movie_title, user_id=request.user.id )
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
    elif sort_by == 'user_id':
        reviews = reviews.order_by('user_id_username') # Sort by Reviewer username
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

@login_required(login_url=reverse_lazy('accounts:login'))   
# Gets all movies with high ratings
def movie_recommendations(request):
    # Get movies that have a rating of 5 and group by movie title
    top_rated_movies = Review.objects.filter(rating=5).values('movie_title').annotate(total_reviews=Count('movie_title')).order_by('-total_reviews')

    # You can pass this list of recommended movies to your template
    context = {
        'top_rated_movies': top_rated_movies
    }

    
    return render(request, 'movie_recommendations.html', context)
    
    

    
        

    


