from django.urls import path
from posts import views

urlpatterns = [
    path('category/<str:category>/', views.category, name='category'),
    path('tag/<str:tag>/', views.tag, name='tag'),
    path('<slug:slug>/', views.detail, name="detail"), #/ないとエラー出る
    path('', views.index, name="index"),
]
