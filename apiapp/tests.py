from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from blog.models import Post


class PostAPIPermissionTests(APITestCase):

    def setUp(self):
        user_model = get_user_model()
        self.regular_user = user_model.objects.create_user(
            username='regular',
            password='test-password',
        )
        self.superuser = user_model.objects.create_superuser(
            username='admin',
            password='test-password',
        )

    def test_anonymous_user_can_read_posts(self):
        response = self.client.get(reverse('post-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_user_cannot_create_post(self):
        response = self.client.post(
            reverse('post-list'),
            {'title': 'title', 'text': 'text'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 0)

    def test_regular_user_cannot_create_post(self):
        self.client.force_authenticate(user=self.regular_user)

        response = self.client.post(
            reverse('post-list'),
            {'title': 'title', 'text': 'text'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 0)

    def test_superuser_can_create_post(self):
        self.client.force_authenticate(user=self.superuser)

        response = self.client.post(
            reverse('post-list'),
            {'title': 'title', 'text': 'text'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
