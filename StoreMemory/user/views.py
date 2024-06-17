from django.shortcuts import render
from .models import Memory
from templates import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
def profile(request):
    title= 'Welcome to Store Memory'
    memories = list_memories(request)
    return render(request, "user/home.html",{
        'title': title,
        'memories': memories
        })

def home(request):
    return render(request, "user/home.html")

def list_memories(request):
    user_id = None
    if request.user.is_authenticated:
        user_id = request.user.id
    if user_id:
        memories_list = Memory.objects.filter(created_by_id=user_id).order_by('-created_at')
    else:
        return render(request, '404.html') 
        
    paginator = Paginator(list(memories_list), 5)  # Show 10 memories per page

    page = request.GET.get('page') if request.GET.get('page') else 1
    
    try:
        memories = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        memories = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        memories = paginator.page(paginator.num_pages)

    return memories
    
    