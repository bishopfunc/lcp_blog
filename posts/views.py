from django.shortcuts import get_object_or_404, redirect, render
from .models import Category, Post, Tag
from django.db.models import Q
from django.contrib import messages
from functools import reduce
from operator import and_
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    # tag = Tag.objects.all()
    posts = Post.objects.order_by('-created_at').filter(draft_flg=False)
    # tag = [post.tag for post in posts]
    return render(request, 'posts/index.html', {'posts': posts})

def search(request):
    posts = Post.objects.order_by('-created_at')
    keyword = request.GET.get('keyword')

    if keyword:
        """ 除外リストを作成 """
        exclusion_list = set([' ', '　'])
        q_list = ''

        for i in keyword:
            """ 全角半角の空文字が含まれていたら無視 """
            if i in exclusion_list:
                pass
            else:
                q_list += i

        query = reduce(
                    and_, [Q(title__icontains=q) | Q(category__name__icontains=q) | Q(tags__name__icontains=q) for q in q_list]
                )
                # fieldなら階層ありでもいける

        posts = posts.filter(query)
        if posts:
            messages.success(request, f'「{keyword}」の検索結果')
            messages.success(request, f'{len(posts)}件の記事が見つかりました')
        else:
            messages.success(request, f'「{keyword}」の検索結果')
            messages.success(request, f'記事が見つかりませんでした')

        return render(request, 'posts/search.html', {'posts': posts, 'keyword': keyword})

    return redirect('index') #keywordが空の場合はindexにリダイレクト


def category(request, category):
    category = Category.objects.get(name=category)
    posts = Post.objects.filter(category=category)
    return render(request, 'posts/tag_category.html', {'category': category, 'posts': posts})

def tag(request, tag):
    tags = Tag.objects.get(name=tag)
    posts = Post.objects.filter(tags=tags)
    return render(request, 'posts/tag_category.html', {'tag': tags, 'posts': posts})

def detail(request, slug):
    # tags = Tag.objects.all()
    if request.user.is_authenticated: #管理者なら全てを表示
        post = get_object_or_404(Post, slug=slug)
    else:
        post = get_object_or_404(Post, slug=slug, draft_flg=False) #一般ユーザーなら下書きでないものを表示
    # for tag in tags:
    #     posts = Post.objects.filter(slug=slug, tag=tag)
    #     for post in posts:
    #         print(post.tag.name)
    return render(request, 'posts/detail.html', {'post': post})

@login_required
def draft(request):
    draft = Post.objects.filter(draft_flg=True)
    return render(request, 'posts/draft.html', {'draft': draft})

def about(request):
    return render(request, 'posts/about.html')

def tag_for_about(request, tag):
    tag = Tag.objects.get(tag=tag)
    return render(request, 'posts/tag_for_about.html', {'tag': tag})

def tag_list(request):
    return render(request, 'posts/tag_list.html')

def contact(request):
    return render(request, 'posts/contact.html')

def top_img(request, text='Welcome To bishopfunc Blog!!'):
    return render(request, 'posts/top_umg.html', {'text': text})