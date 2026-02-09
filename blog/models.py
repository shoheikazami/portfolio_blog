from django.conf import settings
from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField('タイトル', max_length=200)
    image = models.ImageField(upload_to="uploads/", null=True, blank=True)
    text = models.TextField('本文')
    date = models.DateTimeField('日付', default=timezone.now)

    def __str__(self):
        return self.title

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'ip_address')

    def __str__(self):
        return f"{self.ip_address} liked {self.post.title}"

