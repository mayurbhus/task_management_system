from rest_framework.permissions import BasePermission

class TaskPermission(BasePermission):
    """
    Custom permission for Task model:
    - Managers can CRUD tasks in their projects
    - Team members can only read tasks assigned to them
    - Team members can only update status of tasks assigned to them
    """
    
    def has_permission(self, request, view):
        # Must be authenticated
        if not request.user.is_authenticated:
            return False
        
        # Allow all authenticated users to list/read
        if view.action in ['list', 'retrieve']:
            return True
        
        # Only managers can create/delete tasks
        if view.action in ['create', 'destroy']:
            return request.user.role == 'manager'
        
        # Both managers and team members can update (but object level permission will restrict)
        if view.action in ['update', 'partial_update']:
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        # Must be authenticated
        if not request.user.is_authenticated:
            return False
        
        # For read operations
        if view.action in ['retrieve']:
            # Managers can read tasks in their projects
            if request.user.role == 'manager' and obj.created_by == request.user:
                return True
            # Team members can read tasks assigned to them
            if obj.assigned_to == request.user:
                return True
            return False
        
        # For update operations
        if view.action in ['update', 'partial_update']:
            # Managers can update all tasks in their projects
            if request.user.role == 'manager' and obj.created_by == request.user:
                return True
            # Team members can only update their task status
            if obj.assigned_to == request.user:
                return True
            return False
        
        # For delete operations
        if view.action == 'destroy':
            # Only managers can delete tasks
            return (request.user.role == 'manager' and obj.created_by == request.user)
        
        return False