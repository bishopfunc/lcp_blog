from unicodedata import name
from django.shortcuts import get_object_or_404, render
from .models import Category, Post, Tag

# Create your views here.
def index(request):
    posts = Post.objects.order_by('-created_at')
    return render(request, 'posts/index.html', {'posts': posts})

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

