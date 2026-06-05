from django.contrib import admin
from .models import Movie

# Register your models here.
# admin.site.register(Movie)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display=['id', 'title', 'genre', 'actors', 'rating', 'director', 'country', 'producer', 'year']
    search_fields =['title', 'genre']
    list_filter= ['genre']