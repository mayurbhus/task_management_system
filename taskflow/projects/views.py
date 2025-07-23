from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from .models import Project
from .serializers import ProjectSerializer
from .permissions import ProjectPermission

class ProjectViewset(viewsets.ModelViewSet):

    serializer_class = ProjectSerializer
    permission_classes = [ProjectPermission]
    
    filterset_fields = ['status', 'manager', 'team_members']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'start_date', 'end_date']
    ordering = ['-created_at']

    def get_queryset(self):
        """
         Filter queryset based on user role:
        - Managers see their own projects
        - Team members see projects they belong to
        """

        user = self.request.user

        if user.role == 'manager':
            return Project.objects.filter(manager=user)
        else:
            return Project.objects.filter(team_members=user)
        
    def perform_create(self, serailizer):
        serailizer.save(manager=self.request.user)

