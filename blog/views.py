from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import PostCreateForm # forms.py で作ったクラスをimport
from .models import Post, Like


def get_client_ip(request):
    """クライアントのIPアドレスを取得"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


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
        queryset = Post.objects.order_by('-date')  # 降順
        keyword = self.request.GET.get('keyword')   # 検索入力キーワード
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(text__icontains=keyword)
            )  # icontains: 部分一致、大小文字区別なし
        return queryset

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