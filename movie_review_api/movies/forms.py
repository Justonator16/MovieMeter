from django import forms
from .models import Review

#Simple Form to search a movie based on movie_title
class MovieForm(forms.Form):
    movie_title = forms.CharField(required=True ,max_length=100, min_length=2)
    
class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=1, max_value=5)
    class Meta:
        model = Review
        fields = ['review_content', 'rating']
    
