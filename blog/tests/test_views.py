from django.test import RequestFactory, SimpleTestCase, TestCase
from django.urls import reverse
from django.core.cache import cache

from ..models import Post
from ..views import get_client_ip


class ClientIPTests(SimpleTestCase):

    def test_ignores_forwarded_for_header(self):
        request = RequestFactory().get(
            '/',
            HTTP_X_FORWARDED_FOR='203.0.113.10',
            REMOTE_ADDR='192.0.2.10',
        )

        self.assertEqual(get_client_ip(request), '192.0.2.10')

class PostListTests(TestCase):

  def setUp(self):
    """
    テスト環境の準備用メソッド。名前は必ず「setUp」とすること。
    同じテストクラス内で共通で使いたいデータがある場合にここで作成する。
    """
    post1 = Post.objects.create(title='title1', text='text1')
    post2 = Post.objects.create(title='title2', text='text2')

  def test_get(self):
    """GET メソッドでアクセスしてステータスコード200を返されることを確認"""
    response = self.client.get(reverse('blog:post_list'))
    self.assertEqual(response.status_code, 200)
  
  def test_get_2posts_by_list(self):
    """GET でアクセス時に、setUp メソッドで追加した 2件追加が返されることを確認"""
    response = self.client.get(reverse('blog:post_list'))
    self.assertEqual(response.status_code, 200)
    self.assertQuerySetEqual(
      # Postモデルでは __str__ の結果としてタイトルを返す設定なので、返されるタイトルが投稿通りになっているかを確認
      response.context['post_list'],
      ['<Post: title1>', '<Post: title2>'],
      transform=repr,
      ordered = False # 順序は無視するよう指定
    )
    self.assertContains(response, 'title1') # html 内に post1 の title が含まれていることを確認
    self.assertContains(response, 'title2') # html 内に post2 の title が含まれていることを確認

  def tearDown(self):
      """
      setUp で追加したデータを消す、掃除用メソッド。
      create とはなっているがメソッド名を「tearDown」とすることで setUp と逆の処理を行ってくれる＝消してくれる。
      """
      post1 = Post.objects.create(title='title1', text='text1')
      post2 = Post.objects.create(title='title2', text='text2')


class PostSearchTests(TestCase):

    def setUp(self):
        cache.clear()

    def test_search_by_title(self):
        Post.objects.create(title='Django', text='framework')
        Post.objects.create(title='映画', text='作品の感想')

        response = self.client.get(
            reverse('blog:post_list'),
            {'keyword': 'Django'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context['post_list'],
            ['<Post: Django>'],
            transform=repr,
        )

    def test_post_changes_invalidate_cached_results(self):
        Post.objects.create(title='first', text='text')
        self.client.get(reverse('blog:post_list'))

        Post.objects.create(title='second', text='text')
        response = self.client.get(reverse('blog:post_list'))

        self.assertContains(response, 'second')

class PostCreateTests(TestCase):
    """PostCreateビューのテストクラス."""

    def test_get(self):
        """GET メソッドでアクセスしてステータスコード200を返されることを確認"""
        response = self.client.get(reverse('blog:post_create'))
        self.assertEqual(response.status_code, 200)

    def test_post_with_data(self):
        """適当なデータで　POST すると、成功してリダイレクトされることを確認"""
        data = {
            'title': 'test_title',
            'text': 'test_text',
        }
        response = self.client.post(reverse('blog:post_create'), data=data)
        self.assertEqual(response.status_code, 302)
    
    def test_post_null(self):
        """空のデータで POST を行うとリダイレクトも無く 200 だけ返されることを確認"""
        data = {}
        response = self.client.post(reverse('blog:post_create'), data=data)
        self.assertEqual(response.status_code, 200)

class PostDetailTests(TestCase): # 追加
    """PostDetailView のテストクラス"""

    def test_not_fount_pk_get(self):
        """記事を登録せず、空の状態で存在しない記事のプライマリキーでアクセスした時に 404 が返されることを確認"""
        response = self.client.get(
            reverse('blog:post_detail', kwargs={'pk': 1}),
        )
        self.assertEqual(response.status_code, 404)

    def test_get(self):
        """GET メソッドでアクセスしてステータスコード200を返されることを確認"""
        post = Post.objects.create(title='test_title', text='test_text')
        response = self.client.get(
            reverse('blog:post_detail', kwargs={'pk': post.pk}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title)
        self.assertContains(response, post.text)

class PostUpdateTests(TestCase): # 追加
    """PostUpdateView のテストクラス"""

    def test_not_fount_pk_get(self):
        """記事を登録せず、空の状態で存在しない記事のプライマリキーでアクセスした時に 404 が返されることを確認"""
        response = self.client.get(
            reverse('blog:post_update', kwargs={'pk': 1}),
        )
        self.assertEqual(response.status_code, 404)

    def test_get(self):
        """GET メソッドでアクセスしてステータスコード200を返されることを確認"""
        post = Post.objects.create(title='test_title', text='test_text')
        response = self.client.get(
            reverse('blog:post_update', kwargs={'pk': post.pk}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title)
        self.assertContains(response, post.text)

class PostDeleteTests(TestCase): # 追加
    """PostDeleteView のテストクラス"""

    def test_not_fount_pk_get(self):
        """記事を登録せず、空の状態で存在しない記事のプライマリキーでアクセスした時に 404 が返されることを確認"""
        response = self.client.get(
            reverse('blog:post_delete', kwargs={'pk': 1}),
        )
        self.assertEqual(response.status_code, 404)

    def test_get(self):
        """GET メソッドでアクセスしてステータスコード200を返されることを確認"""
        post = Post.objects.create(title='test_title', text='test_text')
        response = self.client.get(
            reverse('blog:post_delete', kwargs={'pk': post.pk}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title)
        self.assertContains(response, post.text)