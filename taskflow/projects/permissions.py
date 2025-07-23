from rest_framework.permissions import BasePermission

class ProjectPermission(BasePermission):
    """
    Custom permission for Project model:
    - Managers can CRUD their own projects
    - Team members can only read projects they belong to
    """
    
    def has_permission(self, request, view):
        # Must be authenticated
        if not request.user.is_authenticated:
            return False
        
        # Allow all authenticated users to list/read
        if view.action in ['list', 'retrieve']:
            return True
        
        # Only managers can create/update/delete projects
        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.role == 'manager'
        
        return False
    
    def has_object_permission(self, request, view, obj):
        # Must be authenticated
        if not request.user.is_authenticated:
            return False
        
        # For read operations
        if view.action in ['retrieve']:
            # Managers can read their own projects
            if request.user.role == 'manager' and obj.manager == request.user:
                return True
            # Team members can read projects they belong to
            if obj.team_members.filter(id=request.user.id).exists():
                return True
            return False
        
        # For write operations (update/delete)
        if view.action in ['update', 'partial_update', 'destroy']:
            # Only managers can modify their own projects
            return (request.user.role == 'manager' and obj.manager == request.user)
        
        return False

