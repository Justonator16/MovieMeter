from django import forms
import datetime as dt
from django.contrib.auth import validators

today = dt.date.today()
#Simple Form to search a movie
class MovieForm(forms.Form):
    movie_title = forms.CharField(required=True ,max_length=100, min_length=2)