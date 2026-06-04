from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    actors = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(10)])
    director = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    producer = models.CharField(max_length=100, blank=True, null=True)
    year = models.IntegerField()
    description = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.title

