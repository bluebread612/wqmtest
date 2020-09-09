from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'index.html')


def stack(request):
    return render(request, 'stack-example.html')
