from django.urls import path
# from .views import UploadView
from posts import views

urlpatterns = [
    path('category/<str:category>/', views.category, name='category'),
    path('draft/', views.draft, name='draft'),
    path('tag/<str:tag>/', views.tag, name='tag'),
    path('tags', views.tag_list, name='tag_list'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('<slug:slug>/', views.detail, name="detail"), #/ないとエラー出る
    path('', views.index, name="index"),

]
