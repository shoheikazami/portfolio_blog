from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from blog.models import Post


class PostAPIPermissionTests(APITestCase):

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
