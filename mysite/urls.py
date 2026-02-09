"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from apiapp.urls import router as api_router
from django.contrib.auth.models import User
from django.http import HttpResponse

from django.conf import settings 
from django.conf.urls.static import static

def create_superuser(request):
    # すでに存在する場合は作らない
    if not User.objects.filter(username="godzilla1954").exists():
        User.objects.create_superuser(
            username="godzilla1954",        # 任意のユーザー名
            email="ryo_naka2_3728@icloud.com",  # 任意のメール
            password="qovsav-rapji9-cupGex"     # 任意のパスワード
        )
        return HttpResponse("Superuser created!")
    return HttpResponse("Superuser already exists.")


urlpatterns = [
    # 管理画面
    path('rider1971/', admin.site.urls),

    # ブログアプリ
    path('blog/', include('blog.urls')),

    # API (router.urls がリストの場合、そのまま include に渡す)
    path('api/', include(api_router.urls)),

    path('create-su/', create_superuser),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

