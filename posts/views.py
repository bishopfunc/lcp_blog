from django.shortcuts import get_object_or_404, redirect, render
from .models import Category, Post, Tag
from django.db.models import Q
from django.contrib import messages
from functools import reduce
from operator import and_

# Create your views here.
def index(request):
    posts = Post.objects.order_by('-created_at')
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
                    and_, [Q(title__icontains=q) | Q(category__name__icontains=q) | Q(tag__name__icontains=q) for q in q_list]
                )
                # fieldなら階層ありでもいける

        posts = posts.filter(query)
        if posts:
            messages.success(request, f'「{keyword}」の検索結果')
            messages.success(request, f'{len(posts)}件の記事が見つかりました')
        else:
            messages.success(request, f'「{keyword}」の検索結果')
            messages.success(request, f'記事が見つかりませんでした')

        return render(request, 'posts/search.html', {'posts': posts})

    return redirect('index') #keywordが空の場合はindexにリダイレクト


def category(request, category):
    category = Category.objects.get(name=category)
    posts = Post.objects.filter(category=category)
    return render(request, 'posts/index.html', {'category': category, 'posts': posts})

def tag(request, tag):
    tag = Tag.objects.get(name=tag)
    posts = Post.objects.filter(tag=tag)
    return render(request, 'posts/index.html', {'tag': tag, 'posts': posts})

def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'posts/detail.html', {'post': post})

