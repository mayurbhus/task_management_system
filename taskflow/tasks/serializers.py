from rest_framework import serializers
from .models import Task
from projects.models import Project
from accounts.models import User

# 1st approach

# class TaskSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Task
#         fields = '__all__'

# 2nd approach
# class TaskSerializer(serializers.ModelSerializer):

#     # Use CharField for input to accept usernames
#     created_by = serializers.CharField(write_only=True)
#     assigned_to = serializers.CharField(write_only=True)
#     project = serializers.CharField(write_only=True)
    
#     # # Read-only fields to return user details in response
#     # manager_detail = UserSerializer(source='manager', read_only=True)
#     # team_members_detail = UserSerializer(source='team_members', many=True, read_only=True)
    
#     class Meta:
#         model = Task
#         # fields = [
#         #     'id', 'name', 'description', 'status', 
#         #     'manager', 'team_members', 'start_date', 'end_date', 
#         #     'created_at', 'manager_detail', 'team_members_detail'
#         # ]
#         # read_only_fields = ['created_at']
#         fields = '__all__'
    
#     def validate_user(self, value):
#         """Convert user to user primary key"""
#         try:
#             user = User.objects.get(username=value)
#             return user
#         except User.DoesNotExist:
#             raise serializers.ValidationError(f"User with username '{value}' does not exist.")
    
#     def validate_project(self, value):
#         """Convert project name to project primary key"""
#         try:
#             project = Project.objects.get(name=value)
#             return project
#         except User.DoesNotExist:
#             raise serializers.ValidationError(f"User with username '{value}' does not exist.")
    
#     def create(self, validated_data):
#         """Create task with manager, team member and project"""
#         manager = validated_data.pop('created_by')
#         team_member = validated_data.pop('assigned_to')
#         project_name = validated_data.pop('project')
        
#         # Create the project
#         # task = Task.objects.create(created_by=manager, assigned_to=team_member, project=project_name, **validated_data)
#         task = Task.objects.create(validated_data)

#         return task

# 3rd approach
# serializers.py

class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(
        slug_field='username',  
        queryset=User.objects.all()
    )
    assigned_to = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )
    project = serializers.SlugRelatedField(
        slug_field='name',  
        queryset=Project.objects.all()
    )

    class Meta:
        model = Task
        fields = '__all__'

    def update(self, instance, validated_data):
        user = self.context['request'].user
        
        # If user is not a manager, restrict updates to status only
        if user.role != 'manager' and instance.assigned_to == user:
            # Team members can only update status and actual_hours
            allowed_fields = ['status']
            restricted_data = {k: v for k, v in validated_data.items() if k in allowed_fields}
            
            for attr, value in restricted_data.items():
                setattr(instance, attr, value)
        else:
            # Managers can update all fields
            assigned_to = validated_data.pop('assigned_to', None)
            created_by = validated_data.pop('created_by', None)
            project = validated_data.pop('project', None)
            
            # Update regular fields
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            
            # Update foreign key fields
            if assigned_to is not None:
                instance.assigned_to = assigned_to
            if created_by is not None:
                instance.created_by = created_by
            if project is not None:
                instance.project = project
        
        instance.save()
        return instance
    
    def create(self, validated_data):
        assigned_to = validated_data.pop('assigned_to')
        created_by = validated_data.pop('created_by')
        project = validated_data.pop('project')
        
        task = Task.objects.create(
            assigned_to=assigned_to,
            created_by=created_by,
            project=project,
            **validated_data
        )
        return task

