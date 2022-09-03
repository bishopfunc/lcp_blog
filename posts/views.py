from django.shortcuts import get_object_or_404, redirect, render
from .models import Category, Post, Tag
from django.db.models import Q
from django.contrib import messages
from functools import reduce
from operator import and_
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.views import generic
from django.utils.decorators import method_decorator


# Create your views here.
def index(request):
    posts = Post.objects.order_by('-created_at').filter(draft_flg=False)
    paginator = Paginator(posts, 10)
    page = request.GET.get('page', 1)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(1)
    return render(request, 'posts/index.html', {'posts': posts, 'pages': pages})

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

        posts = list(set(posts.filter(query))) #重複防止
        if posts:
            print(posts)
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


# class UploadView(generic.View):  
#     """ upload image file """  

#     @method_decorator(csrf_exempt)  
#     def dispatch(self, *args, **kwargs):  
#         return super(UploadView, self).dispatch(*args, **kwargs)  

#     def post(self, request, *args, **kwargs):  
#         upload_image = request.FILES.get("editormd-image-file", None)  
#         print('upload：', upload_image)  
#         media_root = settings.MEDIA_ROOT  

#         # image none check  
#         if not upload_image:  
#             return JsonResponse({  
#                 'success': 0,  
#                 'message': "未获取到要上传的图片",  
#                 'url': ""  
#             })  

#         # image format check  
#         file_name_list = upload_image.name.split('.')  
#         file_extension = file_name_list.pop(-1)  
#         file_name = '.'.join(file_name_list)  
#         if file_extension not in settings.MDEDITOR_CONFIGS['upload_image_formats']:  
#             return JsonResponse({  
#                 'success': 0,  
#                 'message': "上传图片格式错误，允许上传图片格式为：%s" % ','.join(  
#                     settings.MDEDITOR_CONFIGS['upload_image_formats']),  
#                 'url': ""  
#             })  

#         # image floder check  
#         file_path = os.path.join(media_root, settings.MDEDITOR_CONFIGS['image_folder'])  
#         print('上传路径：', file_path)  
#         if not os.path.exists(file_path):  
#             try:  
#                 os.makedirs(file_path)  
#             except Exception as err:  
#                 return JsonResponse({  
#                     'success': 0,  
#                     'message': "上传失败：%s" % str(err),  
#                     'url': ""  
#                 })  

#         # save image  
#         file_full_name = '%s_%s.%s' % (file_name,  
#                                        '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now()),  
#                                        file_extension)  
#         with open(os.path.join(file_path, file_full_name), 'wb+') as file:  
#             for chunk in upload_image.chunks():  
#                 file.write(chunk)  

#         return JsonResponse({'success': 1,  
#                              'message': "上传成功！",  
#                              'url': os.path.join(settings.MEDIA_URL,  
#                                                  settings.MDEDITOR_CONFIGS['image_folder'],  
#                                                  file_full_name)})  