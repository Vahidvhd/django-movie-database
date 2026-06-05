from django.shortcuts import render
from django.db.models import Q
from .models import Movie


def home(request):



    query = request.GET.get('user_search')
    result = Movie.objects.all()
    if query:
        result = Movie.objects.filter (
            Q(title__icontains=query) |
            Q(actors__icontains=query) )
        
    context = {'result': result}
        
    return render(request, "movies/home.html", context)