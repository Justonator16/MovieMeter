from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    movie_title = models.CharField(max_length=50, default="", unique=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    review_content = models.TextField(max_length=100, default="")
    rating = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)