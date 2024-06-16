from django.shortcuts import render
from templates import *
# Create your views here.
def profile(request):
    title= 'Welcome to Store Memory'
    return render(request, "user/home.html",{'title': title})

def home(request):
    return render(request, "user/home.html")