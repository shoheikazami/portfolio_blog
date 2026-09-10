import hashlib

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from django.urls import reverse_lazy
from django.db.models import Case, IntegerField, Q, When
from django.db import connection
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import PostCreateForm # forms.py で作ったクラスをimport
from .models import Post, Like
from .cache import POST_LIST_CACHE_TIMEOUT, get_post_list_cache_version


def get_client_ip(request):
    """接続元ソケットのIPアドレスを取得する。"""
    return request.META.get('REMOTE_ADDR')


@require_POST
def toggle_like(request, pk):
    """いいねの追加/削除"""
    post = get_object_or_404(Post, pk=pk)
    ip = get_client_ip(request)
    
    like, created = Like.objects.get_or_create(post=post, ip_address=ip)
    if not created:
        like.delete()
    
    return JsonResponse({'likes': post.likes.count()})



class PostListView(generic.ListView):
    model = Post
    paginate_by = 5

    def get_queryset(self):
        keyword = self.request.GET.get('keyword', '').strip()
        cache_key = self.get_post_list_cache_key(keyword)
        cached_ids = cache.get(cache_key)
        if cached_ids is not None:
            if not cached_ids:
                return Post.objects.none()
            ordering = [When(pk=post_id, then=position) for position, post_id in enumerate(cached_ids)]
            return Post.objects.filter(pk__in=cached_ids).order_by(
                Case(*ordering, output_field=IntegerField())
            )

        queryset = Post.objects.order_by('-date')  # 降順
        if keyword:
            if connection.vendor == 'postgresql':
                search_vector = (
                    SearchVector('title', weight='A')
                    + SearchVector('text', weight='B')
                )
                search_query = SearchQuery(keyword, search_type='websearch')
                queryset = (
                    queryset
                    .annotate(search=search_vector, rank=SearchRank(search_vector, search_query))
                    .filter(search=search_query)
                    .order_by('-rank', '-date')
                )
            else:
                queryset = queryset.filter(
                    Q(title__icontains=keyword) | Q(text__icontains=keyword)
                )  # SQLite開発環境では部分一致検索にフォールバック

        post_ids = list(queryset.values_list('pk', flat=True))
        cache.set(cache_key, post_ids, timeout=POST_LIST_CACHE_TIMEOUT)
        return queryset

    def get_post_list_cache_key(self, keyword):
        keyword_hash = hashlib.sha256(keyword.casefold().encode('utf-8')).hexdigest()
        version = get_post_list_cache_version()
        return f'blog:post-list:{version}:{keyword_hash}'

class PostCreateView(LoginRequiredMixin, UserPassesTestMixin,generic.CreateView): # 追加
    model = Post # 作成したい model を指定
    form_class = PostCreateForm # 作成した form クラスを指定
    success_url = reverse_lazy('blog:post_list') # 記事作成に成功した時のリダイレクト先を指定
    def test_func(self):
        return self.request.user.is_superuser



class PostDetailView(generic.DetailView):
    model = Post

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView): # 追加
    model = Post
    form_class = PostCreateForm # PostCreateFormをほぼそのまま活用できる
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView): # 追加
    model = Post
    success_url = reverse_lazy('blog:post_list')
    def test_func(self):
        return self.request.user.is_superuser