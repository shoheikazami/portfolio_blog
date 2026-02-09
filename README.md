# Djangoブログアプリ
# 概要
Djangoを用いて開発した個人用ブログアプリです。私の好きな本・映画・特撮作品の感想を書くために作りました。
CRUD機能や検索機能など、実用的な機能を実装しています。renderでデプロイもしたのですが管理画面にログインできず、解決するには有料版を使わなければならなかったので仕方なく断念しました。

# 主な機能
-　ユーザー認証機能（スーパーユーザーしか記事を投稿・編集・削除できない）
-　記事の投稿/編集/削除
-　いいね機能
-　記事検索機能
-　管理者機能

# 使用技術
- python 3.0
- Django
- SQLite (開発環境)
- HTML/bootstrap CSS
- Git / GitHub

# 工夫した点
- REST API化によるフロントエンドとの分離(実装に苦労したが、Github Copilotの協力で可能となった)
- セキュリティ対策(csrf)
- 基本的な機能に対するテストコードの実装

# 環境構築方法
- '''bash
- git clone https://github.com/shoheikazami/portfolio_blog
- cd portfolio_blog
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py runserver

# 参考記事
https://zenn.dev/tmasuyama1114/articles/django-tutorial-blogapp-1
https://zenn.dev/tmasuyama1114/articles/django-tutorial-blogapp-2
https://zenn.dev/tmasuyama1114/articles/django-tutorial-blogapp-3
https://zenn.dev/tmasuyama1114/articles/django-tutorial-blogapp-4
https://zenn.dev/tmasuyama1114/articles/django-tutorial-blogapp-5
https://zenn.dev/tmasuyama1114/articles/django-tutorial-blogapp-6
https://zenn.dev/tmasuyama1114/articles/django-tutorial-blogapp-7
https://qiita.com/Kmashi/items/b9136e7e422f4432a314
https://zenn.dev/animalz/articles/ea26c757a01abb
https://qiita.com/tatsuya11bbs/items/53620db6cd0e1e3bb12a
https://qiita.com/hayato0311/items/c4400dd04f8da5ad9390

# 感想と課題
初めてDjangoでブログアプリを作ることができた。
ただしAI(GitHub Copilot)に頼ってしまったことや二段階認証、Docker化ができなかったことなどがあるのでそれは今後の課題とする。
