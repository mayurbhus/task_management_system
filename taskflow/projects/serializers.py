from rest_framework import serializers
from .models import Project
from accounts.models import User
# 1st approach

# class ProjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Project
#         fields = '__all__'

# 2nd approach
# class ProjectSerializer(serializers.ModelSerializer):
#     # Use CharField for input to accept usernames
#     manager = serializers.CharField(write_only=True)
#     team_members = serializers.ListField(
#         child=serializers.CharField(), 
#         write_only=True, 
#         required=False
#     )
    
#     # # Read-only fields to return user details in response
#     # manager_detail = UserSerializer(source='manager', read_only=True)
#     # team_members_detail = UserSerializer(source='team_members', many=True, read_only=True)
    
#     class Meta:
#         model = Project
#         # fields = [
#         #     'id', 'name', 'description', 'status', 
#         #     'manager', 'team_members', 'start_date', 'end_date', 
#         #     'created_at', 'manager_detail', 'team_members_detail'
#         # ]
#         # read_only_fields = ['created_at']
#         fields = '__all__'
    
#     def validate_manager(self, value):
#         """Convert manager username to User object"""
#         try:
#             manager = User.objects.get(username=value)
#             return manager
#         except User.DoesNotExist:
#             raise serializers.ValidationError(f"User with username '{value}' does not exist.")
    
#     def validate_team_members(self, value):
#         """Convert team member usernames to User objects"""
#         if not value:
#             return []
        
#         users = []
#         for username in value:
#             try:
#                 user = User.objects.get(username=username)
#                 users.append(user)
#             except User.DoesNotExist:
#                 raise serializers.ValidationError(f"User with username '{username}' does not exist.")
        
#         return users
    
#     def create(self, validated_data):
#         """Create project with manager and team members"""
#         manager = validated_data.pop('manager')
#         team_members = validated_data.pop('team_members', [])
        
#         # Create the project
#         project = Project.objects.create(manager=manager, **validated_data)
        
#         # Add team members
#         if team_members:
#             project.team_members.set(team_members)
        
#         return project

# 3rd approach

class ProjectSerializer(serializers.ModelSerializer):
    manager = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )
    team_members = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        many=True
    )
    
    class Meta:
        model = Project
        fields = '__all__'