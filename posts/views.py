from django.shortcuts import get_object_or_404, render
from .models import Post

# Create your views here.
def index(request):
    print(f'request: {request.body}')
    posts = Post.objects.order_by('-created_at')
    return render(request, 'posts/index.html', {'posts': posts})

def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'posts/detail.html', {'post': post})
