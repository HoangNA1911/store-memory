from django.urls import path, include
from user import views
urlpatterns = [
    path("", views.profile,name="home" ),
    path("add-memory/",views.add_memory,  name='add-memory'),
    path("memory/<int:pk>",views.memory_detail,name = 'memory-detail'),
    path("memory/<int:pk>/edit",views.edit_memory,name = 'edit-memory'),
    path("memory/<int:pk>/delete",views.delete_memory,name = 'delete-memory')
]