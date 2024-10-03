import requests

def MovieInfoToJson(movie_title: str):
    #Limited to 1000 requests daily
    #juniorjusto16@gmail.com
    api_key = '3f605626'
    #juniojusto42@gmail.com
    api_key_2 = 'cf45ee53'
    
    #In case the api key requests have reach 1000
    #Or theres an error in connection of the first api
    try:
        #Json of all movies that fit the parameter                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      nd with the parameter provided in the url
        url = f'http://www.omdbapi.com/?apikey={api_key}&s={movie_title}&plot=short'
    except:
        #Return json of all movies fou                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      nd with the parameter provided in the url
        url = f'http://www.omdbapi.com/?apikey={api_key_2}&s={movie_title}&plot=short'
    
    result = requests.get(url)
    search_results = result.json()
    

    #Returns a dictionary of all movies that match url request
    try:
        movie_info_json = search_results['Search']
    except:
        return None
    
    return movie_info_json

def get_movie_detail(title : str):
    api_key = '3f605626' 
    api_key_2 = 'cf45ee53'

    try:
        # Get movie details
        # Returns a dictionary of movie details eg plot, ratings,director, release date
        url = f'http://www.omdbapi.com/?apikey={api_key}&t={title}'
    except:
        # Get movie details
        # Returns a dictionary of movie details eg plot, ratings,director, release date
        url = f'http://www.omdbapi.com/?apikey={api_key_2}&t={title}'
        
    result = requests.get(url)
    movie_detail = result.json()

    # Returns a dictionary of all details in movie
    return movie_detail

def get_popular_movies(num):
    #Trakt API 
    url = f'https://api.trakt.tv/movies/popular?limit={num}'
    result = requests.get(url)
    
    #API might return an error , 
    try:
        movies_json = result.json()
    except:
        #If theres an error on the Trakt API then l will try the OMDBAPI
        movies_json = MovieInfoToJson('Avengers')
    
    return movies_json

def sort_movies_asc(movie_title_and_rating_dict: dict):
    # Sorting the dictionary by its values in ascending order
    sorted_dict = dict(sorted(movie_title_and_rating_dict.items(), key=lambda item: item[1]))
    return sorted_dict
    
def filter_search_results(search_results_list=None, filter_by=None ):
    if search_results_list == None or filter_by == None:
        return None
    
    #Returns only movies list
    elif filter_by == 'only_movies':
        only_movies_list = [ item for item in search_results_list if item['Type'] == 'movie']
        return only_movies_list
    
    elif filter_by == 'only_series':
        only_series_list = [ item for item in search_results_list if item['Type'] == 'series']
        return only_series_list
    
    elif filter_by == 'imdb_rating':
        #First get all imdb_ratings of movie
        imdb_ratings = {}
        for item in search_results_list:
            for rating in item['Ratings']:
                #Some movies dont have ratings or have not been rated
                try:
                    if rating['Source'] == 'Internet Movie Database':
                        movie_title_rating_pair =  { item['Title'] : int(rating['Value']) }
                        imdb_ratings.update(movie_title_rating_pair)
                except:
                    movie_title_rating_pair = { item['Title'] : 1}
                    imdb_ratings.update(movie_title_rating_pair) 
        
        sorted_movies = sort_movies_asc(imdb_ratings)
        sorted_movies_full_detail = [ get_movie_detail(movie) for movie in sorted_movies ]           

        return sorted_movies_full_detail
    
    elif filter_by == 'rotten_tomatoes_rating':
        #First get all imdb_ratings of movie
        rotten_tomatoes_ratings = {}
        for item in search_results_list:
            for rating in item['Ratings']:
                #Some movies dont have ratings or have anot been rated
                try:
                    if rating['Source'] == 'Rotten Tomatoes':
                        movie_title_rating_pair =  { item['Title'] : int(rating['Value']) }
                        rotten_tomatoes_ratings.update(movie_title_rating_pair)
                except:
                    movie_title_rating_pair = { item['Title'] : 1}
                    rotten_tomatoes_ratings.update(movie_title_rating_pair)
                    
        sorted_movies = sort_movies_asc(rotten_tomatoes_ratings)
        sorted_movies_full_detail = [ get_movie_detail(movie) for movie in sorted_movies ]           

        return sorted_movies_full_detail
        
    elif filter_by == 'metacritic_rating':
        #First get all imdb_ratings of movie
        metacritic_ratings = {}
        for item in search_results_list:
            for rating in item['Ratings']:
                #Some movies dont have ratings or have anot been rated
                try:
                    if rating['Source'] == 'Metacritic':
                        movie_title_rating_pair =  { item['Title'] : int(rating['Value'] )}
                        metacritic_ratings.update(movie_title_rating_pair)
                except:
                    movie_title_rating_pair = { item['Title'] : 1}
                    metacritic_ratings.update(movie_title_rating_pair)
        
        sorted_movies = sort_movies_asc(metacritic_ratings)
        sorted_movies_full_detail = [ get_movie_detail(movie) for movie in sorted_movies ]           

        return sorted_movies_full_detail
       
    elif filter_by == 'metascore_rating':
        #First get all imdb_ratings of movie
        metascore_ratings = {}
        for item in search_results_list:
            try:
                if item['Metascore']:
                    movie_title_rating_pair = {item['Title']: int(item['Metascore'])}
                    metascore_ratings.update(movie_title_rating_pair)
            except:
                movie_title_rating_pair = {item['Title']: 1}
                metascore_ratings.update(movie_title_rating_pair)
        
        sorted_movies = sort_movies_asc(metascore_ratings)
        sorted_movies_full_detail = [ get_movie_detail(movie) for movie in sorted_movies ]           

        return sorted_movies_full_detail


                

            
        
    
                    
                    
                
        