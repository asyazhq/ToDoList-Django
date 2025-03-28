from django.urls import path, re_path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from . import views
from . import urls_name, urls_auth
from .views import ListUserTasks, TaskDetail, ListUser, DetailUser, TaskViewSet

# Create a router and register the viewset
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')  # Enables automatic URL generation

urlpatterns = [
    path("tasks/", ListUserTasks.as_view(), name="user-tasks"),  # List & create tasks
    path("tasks/<int:pk>/", TaskDetail.as_view(), name="task-detail"),  # Retrieve, update, delete task
    path("tasks/<int:pk>/mark_completed/", TaskViewSet.as_view({'patch': 'mark_completed'}), name="task-mark-completed"),  # Custom PATCH endpoint
    path("users/", ListUser.as_view(), name="user-list"),  # List & create users
    path("users/<int:pk>/", DetailUser.as_view(), name="user-detail"),  # Retrieve, update, delete user
]

# Add authentication URLs
urlpatterns += urls_auth.urlpatterns

# Enable format suffix patterns for API flexibility
urlpatterns = format_suffix_patterns(urlpatterns)

# Include router-generated URLs
urlpatterns += router.urls
