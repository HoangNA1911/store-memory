from django.shortcuts import render,get_object_or_404
from .models import Memory
from templates import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from allauth.socialaccount.models import SocialAccount

def getAvatarUser(request):
    social_account = SocialAccount.objects.filter(user=request.user, provider='google').first()
    avatar_url = social_account.get_avatar_url() if social_account else None
    return avatar_url

def profile(request):
    memories = list_memories(request)
    
    if request.user.is_authenticated:
        avatar_url= getAvatarUser(request)
        return render(request, "user/home.html",{
            'memories': memories,
            'avatar': avatar_url})
    else:
        return render(request, "user/home.html",{
            'memories': memories})
        
def list_memories(request):
    user_id = None
    if request.user.is_authenticated:
        user_id = request.user.id
    if user_id:
        memories_list = Memory.objects.filter(created_by_id=user_id).order_by('-created_at')
    else:
        return render(request, 'user/404.html') 
        
    paginator = Paginator(list(memories_list), 6)  # Show 10 memories per page

    page = request.GET.get('page') if request.GET.get('page') else 1
    
    try:
        memories = paginator.page(page)
    except PageNotAnInteger:
        memories = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        memories = paginator.page(paginator.num_pages)

    return memories

@csrf_exempt
def add_memory(request):
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title')
            description = data.get('description')
            date = data.get('date')
            longitude= data.get('longitude')
            latitude= data.get('latitude')
            if not title or not description or not date :
                return JsonResponse({'error': 'All fields are required.'}, status=400)
            memory = Memory(
                title=title,
                description=description,
                longitude=longitude,
                latitude=latitude,
                created_by=request.user,
                updated_by=request.user
            )
            memory.save()

            return JsonResponse({'message': 'Memory added successfully!'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
    else:
        if request.user.is_authenticated:
            avatar_url= getAvatarUser(request)
        return render(request, 'user/add_memory.html',{'avatar': avatar_url})
        
    

def memory_detail(request, pk):
    memory = get_object_or_404(Memory, pk=pk)
    if request.method == "POST":
        data = json.loads(request.body)
        memory.title = data.get('title')
        memory.description = data.get('description')
        memory.longitude = data.get('Longitude')
        memory.latitude = data.get('Latitude')
        memory.updated_by = request.user
        memory.save()
        return JsonResponse({'message': 'Memory updated successfully!'}, status=200)
    else:
        if request.user.is_authenticated:
            avatar_url= getAvatarUser(request)
        return render(request, 'user/detail_memory.html',{'memory':memory, 'avatar':avatar_url})

def edit_memory(request,pk):
    memory = get_object_or_404(Memory, pk=pk)

    if request.method == 'POST':
        data = json.loads(request.body)
        memory.title = data.get('title')
        memory.description = data.get('description')
        memory.longitude = data.get('longitude')
        memory.latitude = data.get('latitude')
        memory.updated_by = request.user
        memory.created_by = memory.created_by
        memory.save()
        
        return JsonResponse({'message': 'Memory updated successfully!'}, status=200)
    else:
        if request.user.is_authenticated:
            avatar_url= getAvatarUser(request)
        return render(request, 'edit_memory.html', {'memory': memory, 'avatar': avatar_url})


def delete_memory(request,pk):
    memory = get_object_or_404(Memory, pk=pk)

    if request.method == 'POST':
        memory.delete()
        return JsonResponse({'message': 'Memory deleted successfully!'}, status=200)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
    