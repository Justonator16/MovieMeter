import requests
import datetime as dt
from pprint import pprint

today = dt.date.today()
def MovieInfoToJson(movie_title: str) -> dict:
    # Might expire soon! Limited to 1000 requests
    api_key = '3f605626'
    
    #Return json of all movies found with the parameter provided in the url
    url = f'http://www.omdbapi.com/?apikey={api_key}&s={movie_title}&plot=short'
    result = requests.get(url)

    search_results = result.json()

    #Returns a dictionary of all movies that match url request
    movie_info_json = search_results['Search']
    return movie_info_json

def get_movie_detail(title : str):
    api_key = '3f605626'
    
    # Get movie details
    # Returns a dictionary of movie details eg plot, ratings,director, release date
    url = f'http://www.omdbapi.com/?apikey={api_key}&t={title}'
    result = requests.get(url)
    
    movie_detail = result.json()

    # Returns a dictionary of all details in movie
    return movie_detail
