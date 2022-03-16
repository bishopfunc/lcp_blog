from .models import Category, Tag

def related(request):
    context = {
      'category_list': Category.objects.all(),
      'tag_list': Tag.objects.all(),
    }
    return context

# カテゴリーの一覧を取得し表示する category_list
# category.viewはurlに埋め込んだワードをフィルタリングする機能
# urlから取得したcategoryをif文で表示させている
# category.viewでpostsをフィルタリング済みだから、カテゴリーに一致したものしか表示されない