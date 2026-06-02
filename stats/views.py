from django.shortcuts import render
from .models import Standing


def standings(request):
    table = Standing.objects.all().order_by('-points')

    return render(request, 'statistics/standings.html', {
        'table': table
    })

# Create your views here.
