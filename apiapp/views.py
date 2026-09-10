from django.shortcuts import render
from rest_framework import filters, permissions, viewsets
from blog.models import Post
from .serializers import PostSerializer


class PostAPIView(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-date')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'text']
    ordering_fields = ['date', 'title']

