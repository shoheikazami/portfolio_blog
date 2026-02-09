from django.urls import path
from rest_framework import routers
from .views import PostAPIView

router = routers.DefaultRouter()
router.register(r'posts', PostAPIView)

