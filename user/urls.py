# urls.py (within your app directory)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'user', CustomUserViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
