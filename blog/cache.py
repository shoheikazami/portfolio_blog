from django.core.cache import cache


POST_LIST_CACHE_VERSION_KEY = 'blog:post-list:version'
POST_LIST_CACHE_TIMEOUT = 300
POST_LIST_CACHE_VERSION_TIMEOUT = 60 * 60 * 24 * 365 * 10


def get_post_list_cache_version():
    return cache.get_or_set(
        POST_LIST_CACHE_VERSION_KEY,
        1,
        timeout=POST_LIST_CACHE_VERSION_TIMEOUT,
    )


def invalidate_post_list_cache():
    try:
        cache.incr(POST_LIST_CACHE_VERSION_KEY)
    except ValueError:
        cache.add(
            POST_LIST_CACHE_VERSION_KEY,
            1,
            timeout=POST_LIST_CACHE_VERSION_TIMEOUT,
        )