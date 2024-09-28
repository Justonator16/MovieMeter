from django import forms

#Simple Form to search a movie based on movie_title
class MovieForm(forms.Form):
    movie_title = forms.CharField(required=True ,max_length=100, min_length=2)
