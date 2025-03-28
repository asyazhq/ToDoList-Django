from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import TodoListModel, UserModel
from .serializers import TodoListSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied

# Retrieve all tasks belonging to the authenticated user
class ListUserTasks(generics.ListCreateAPIView):
    """
    Endpoint to list all tasks of the authenticated user.
    Allows creating new tasks.
    """
    serializer_class = TodoListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def get_queryset(self):
        queryset = TodoListModel.objects.filter(owner=self.request.user)
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status__iexact=status)  # Case-insensitive filtering
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# Retrieve, update, or delete a task (only if the user is the owner)
class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Endpoint to retrieve, update, or delete a task.
    Only the owner can update or delete their task.
    """
    queryset = TodoListModel.objects.all()  # Fetch all tasks
    serializer_class = TodoListSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        """
        Ensure users can only access their own tasks, returning 403 instead of 404.
        """
        obj = super().get_object()
        if obj.owner != self.request.user:
            raise PermissionDenied("You do not have permission to modify this task.")  # Returns 403
        return obj
    

# User Registration
class ListUser(generics.ListCreateAPIView):
    """
    Endpoint to list users or create a new user.
    """
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Open for registration

# User Profile Management
class DetailUser(generics.RetrieveUpdateDestroyAPIView):
    """
    Endpoint to retrieve, update, or delete user profile.
    Users can only update their own profiles.
    """
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserModel.objects.filter(id=self.request.user.id)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = TodoListModel.objects.all()
    serializer_class = TodoListSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    filter_backends = [filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'description']
    ordering_fields = ['created', 'status']
    filterset_fields = ['status']

    @action(detail=True, methods=['patch'])
    def mark_completed(self, request, pk=None):
        """Custom endpoint to mark a task as completed"""
        task = self.get_object()

        # Ensure the user is the owner before updating
        if task.owner != request.user:
            return Response({'error': 'You do not have permission to modify this task.'}, status=status.HTTP_403_FORBIDDEN)

        task.status = 'completed'  # Match the model's choices exactly
        task.save()
        return Response(TodoListSerializer(task).data, status=status.HTTP_200_OK)
