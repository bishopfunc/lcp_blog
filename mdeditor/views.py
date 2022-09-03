# -*- coding:utf-8 -*-
import os
import datetime

from django.views import generic
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .configs import MDConfig

# TODO 此处获取default配置，当用户设置了其他配置时，此处无效，需要进一步完善
MDEDITOR_CONFIGS = MDConfig('default')


class UploadView(generic.View):
    """ upload image file """

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(UploadView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        upload_image = request.FILES.get("editormd-image-file", None)
        media_root = settings.MEDIA_ROOT

        # image none check
        if not upload_image:
            return JsonResponse({
                'success': 0,
                'message': "未获取到要上传的图片",
                'url': ""
            })

        # image format check
        file_name_list = upload_image.name.split('.')
        file_extension = file_name_list.pop(-1)
        file_name = '.'.join(file_name_list)
        if file_extension not in MDEDITOR_CONFIGS['upload_image_formats']:
            return JsonResponse({
                'success': 0,
                'message': "上传图片格式错误，允许上传图片格式为：%s" % ','.join(
                    MDEDITOR_CONFIGS['upload_image_formats']),
                'url': ""
            })

        # image floder check
        file_path = os.path.join(media_root, MDEDITOR_CONFIGS['image_folder'])
        if not os.path.exists(file_path):
            try:
                os.makedirs(file_path)
            except Exception as err:
                return JsonResponse({
                    'success': 0,
                    'message': "上传失败：%s" % str(err),
                    'url': ""
                })

        # save image
        file_full_name = '%s_%s.%s' % (file_name,
                                       '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now()),
                                       file_extension)
        with open(os.path.join(file_path, file_full_name), 'wb+') as file:
            for chunk in upload_image.chunks():
                file.write(chunk)

        return JsonResponse({'success': 1,
                             'message': "上传成功！",
                             'url': os.path.join(settings.MEDIA_URL,
                                                 MDEDITOR_CONFIGS['image_folder'],
                                                 file_full_name)})

class Cloudinary:
    def __init__(self):  
        self.cloud_name = settings.CLOUDINARY['cloud_name']  
        self.api_key = settings.CLOUDINARY['api_key']  
        self.api_secret = settings.CLOUDINARY['api_secret']  

    def upload(self, key, local_file):  
        import cloudinary
        cloudinary.config(
            cloudname=self.cloud_name,
            api_key=self.api_key,
            api_secret=self.api_secret,
            secure=True)
        import cloudinary.uploader
        import cloudinary.api
        cloudinary.uploader.upload(open(local_file, 'rb'))



class UploadCloudinaryView(generic.View):
    """ upload image file """
    @method_decorator(csrf_exempt)  
    def dispatch(self, *args, **kwargs):  
        return super(UploadCloudinaryView, self).dispatch(*args, **kwargs)  

    def post(self, request, *args, **kwargs):  
        upload_image = request.FILES.get("editormd-image-file", None)  
        media_root = settings.MEDIA_ROOT  

        # image none check  
        if not upload_image:  
            return JsonResponse({  
                'success': 0,  
                'message': "未获取到要上传的图片",  
                'url': ""  
            })  

        # image format check  
        file_name_list = upload_image.name.split('.')  
        file_extension = file_name_list.pop(-1)  
        file_name = '.'.join(file_name_list)  
        if file_extension not in MDEDITOR_CONFIGS['upload_image_formats']:  
            return JsonResponse({  
                'success': 0,  
                'message': "上传图片格式错误，允许上传图片格式为：%s" % ','.join(  
                    MDEDITOR_CONFIGS['upload_image_formats']),  
                'url': ""  
            })  

        # image floder check  
        file_path = os.path.join(media_root, MDEDITOR_CONFIGS['image_folder'])  
        if not os.path.exists(file_path):  
            try:  
                os.makedirs(file_path)  
            except Exception as err:  
                return JsonResponse({  
                    'success': 0,  
                    'message': "上传失败：%s" % str(err),  
                    'url': ""  
                })  

        # 图片重命名  
        file_full_name = '%s_%s.%s' % (file_name,  
                                       '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now()),  
                                       file_extension)  

        #把文件写入本地  
        with open(os.path.join(file_path, file_full_name), 'wb+') as file:  
            for chunk in upload_image.chunks():  
                file.write(chunk)  

        url = os.path.join(settings.MEDIA_URL, MDEDITOR_CONFIGS['image_folder'], file_full_name)  
        # 上传的文件：绝对路径  
        local_file = file_path + '/' + file_full_name  
        # 将原始文件名作为key传给COS  
        key = file_name_list[0] + '.' + file_extension  
        # 调用COS上传文件，返回url  
        upload = Cloudinary().upload(local_file, key)  

        return JsonResponse({'success': 1,  
                             'message': "上传成功！",  
                             'url': upload                               
                            })  