from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Project(models.Model):
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('active', 'Active'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_project')
    team_members = models.ManyToManyField(User, related_name='projects', blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
