from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewset

router = DefaultRouter()
router.register(r'tasks', TaskViewset, basename='task')
urlpatterns = router.urls


