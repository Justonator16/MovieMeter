from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    movie_title = models.CharField(max_length=50, default="", unique=False)
    reviewer = models.ForeignKey(User, on_delete=models.DO_NOTHING, default="")
    review_content = models.CharField(max_length=100, default="")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
        )
    created_at = models.DateField(auto_now_add=True)