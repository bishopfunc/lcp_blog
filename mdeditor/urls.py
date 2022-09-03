import django  

from .views import UploadView, UploadCloudinaryView  

if django.VERSION[0] > 1:  
    from django.urls import re_path as url_func  
else:  
    from django.conf.urls import url as url_func  


urlpatterns = [  
    url_func(r'^uploadlocal/$', UploadView.as_view(), name='uploads'),  # 本地上传，走原来的view  
    url_func(r'^uploads/$', UploadCloudinaryView.as_view(), name='uploads'), # COS上传，走新写的view  
]  