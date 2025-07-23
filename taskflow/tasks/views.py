from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from .models import Task
from .serializers import TaskSerializer
from .perminssions import TaskPermission

class TaskViewset(viewsets.ModelViewSet):

    serializer_class = TaskSerializer
    permission_classes = [TaskPermission]

    filterset_fields = ['project', 'assigned_to', 'created_by', 'priority', 'status']
    search_fields = ['title', 'description']
    ordering = ['-due_date']

    def get_queryset(self):
        """
        This view should return a list of all the tasks
        for the currently authenticated user.
        """
        user = self.request.user

        if user.role == 'manager':
            return Task.objects.filter(created_by=user)
        else:
            return Task.objects.filter(assigned_to=user)


        
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """
        Special endpoint for team members to update only status of their tasks
        """
        task = self.get_object()
        
        # Check if user can update this task
        if request.user.role != 'manager' and task.assigned_to != request.user:
            return Response(
                {'error': 'You can only update status of tasks assigned to you'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        new_status = request.data.get('status')
        if not new_status:
            return Response(
                {'error': 'Status is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate status choice
        valid_statuses = [choice[0] for choice in Task.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return Response(
                {'error': f'Invalid status. Valid choices: {valid_statuses}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        task.status = new_status
        task.save()
        
        return Response(TaskSerializer(task).data)

    