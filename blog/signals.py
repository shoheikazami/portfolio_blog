from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .cache import invalidate_post_list_cache
from .models import Post


@receiver(post_save, sender=Post)
@receiver(post_delete, sender=Post)
def invalidate_post_list_cache_on_change(sender, instance, **kwargs):
    invalidate_post_list_cache()