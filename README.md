# Djangoブログアプリ

Djangoで作成した個人用ブログアプリです。本・映画・特撮作品の感想を投稿できます。

## 主な機能

- ユーザー認証
- スーパーユーザー限定の記事作成・編集・削除
- 記事一覧、詳細表示、キーワード検索
- IPアドレスを利用したいいね機能
- Django REST Frameworkによる記事API
- Django管理画面

APIは記事の閲覧を公開し、作成・更新・削除をスーパーユーザーだけに制限しています。テンプレート側の操作権限も同じルールです。

## 使用技術

- Python 3.13
- Django 5.0
- Django REST Framework
- SQLite（ローカル開発）
- PostgreSQL（`DATABASE_URL` が設定された本番環境）
- Redis（`REDIS_URL` が設定された本番環境のキャッシュ）
- Bootstrap
- WhiteNoise

## ローカル環境の構築

Python 3.10以上を用意してください。

```bash
git clone https://github.com/shoheikazami/portfolio_blog.git
cd portfolio_blog
python -m venv .venv
```

Windows PowerShellの場合:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linuxの場合:

```bash
source .venv/bin/activate
```

依存関係をインストールし、環境変数を設定します。

```bash
python -m pip install -r requirements.txt
copy .env.example .env       # Windows
# cp .env.example .env       # macOS/Linux
```

ローカルでは `.env` の `DATABASE_URL` を削除するとSQLiteを使用できます。`SECRET_KEY` は必ず自分用の値へ変更してください。

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

ブラウザで `http://127.0.0.1:8000/blog/post_list` を開きます。管理画面は `http://127.0.0.1:8000/rider1971/` です。

## API

記事APIのベースURLは `/api/posts/` です。

- `GET /api/posts/`: 記事一覧
- `GET /api/posts/<id>/`: 記事詳細
- `POST /api/posts/`: スーパーユーザーのみ
- `PUT/PATCH /api/posts/<id>/`: スーパーユーザーのみ
- `DELETE /api/posts/<id>/`: スーパーユーザーのみ

検索は `?search=キーワード`、並び替えは `?ordering=title` または `?ordering=date` を使用します。

## キャッシュ設計

記事一覧と検索結果は、検索条件ごとの記事IDと表示順をRedisに5分間キャッシュします。HTML全体ではなく記事IDだけをキャッシュするため、スーパーユーザー向けの編集・削除リンクが他のユーザーへ混ざりません。記事本文やいいね数は通常どおりデータベースから取得します。

記事の保存・更新・削除時にはキャッシュバージョンを繰り上げます。キーに新しいバージョンを含めることで、一覧と全検索条件を一括で無効化し、古いキーはTTL経過後にRedisから削除されます。

## 本番環境

Renderなどのホスティングサービスでは、次の環境変数を設定してください。

- `SECRET_KEY`: 本番用のランダムな秘密鍵
- `DATABASE_URL`: PostgreSQLの接続URL
- `DEBUG`: `False`
- `ALLOWED_HOSTS`: カンマ区切りの許可ホスト名
- `REDIS_URL`: Redisの接続URL

`build.sh` が依存関係のインストール、静的ファイル収集、マイグレーションを実行します。本番環境では管理者を自動作成せず、必要に応じてホスティングサービスのシェルから `python manage.py createsuperuser` を実行してください。

## テスト

```bash
python manage.py check
python manage.py test
```

## 参考記事

- [Djangoブログチュートリアル](https://zenn.dev/tmasuyama1114/articles/django-tutorial-blogapp-1)
- [Django REST framework](https://www.django-rest-framework.org/)
