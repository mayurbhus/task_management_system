from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views 

# router = DefaultRouter()
# router.register(r'users', UserViewset)
# urlpatterns = router.urls

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile')
]