from django.contrib import messages
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'name',
        'USER': 'user',
        'PASSWORD': '',
        'HOST': 'host',
        'PORT': '',
    }
}
try:
    from .local_settings import *
except ImportError:
    pass

ALLOWED_HOSTS = ['127.0.0.1', '.herokuapp.com', 'localhost']

INSTALLED_APPS = [
    'posts.apps.PostsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary', # 追加
    'cloudinary_storage', # 追加
    'mdeditor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' # ??

X_FRAME_OPTIONS = 'SAMEORIGIN' #3.0以上のみ

ROOT_URLCONF = 'lcp_blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'posts.context.related',
            ],
        },
    },
]

WSGI_APPLICATION = 'lcp_blog.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_TZ = True

# media set
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# static set
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
	
#django-mdeditor配置  
MDEDITOR_CONFIGS = {  
'default':{  
    'width': '90%',  # 自定义编辑框宽度  
    'heigth': 1200,   # 自定义编辑框高度  
    'toolbar': ["undo", "redo", "|",  
                "bold", "del", "italic", "quote", "ucwords", "uppercase", "lowercase", "|",  
                #"h1", "h2", "h3", "h5", "h6", "|",  
                "list-ul", "list-ol", "hr", "|",  
                "link", "reference-link", "image", "code", "preformatted-text", "code-block", "table", "datetime",  
                "emoji", "html-entities", "pagebreak", "goto-line", "|",  
                "help", #"info",  
                "||", "uploadToCloudinary", "preview", "watch", "fullscreen"],  # 自定义编辑框工具栏  
    'upload_image_formats': ["jpg", "jpeg", "gif", "png", "bmp", "webp"],  # 图片上传格式类型  
    'image_folder': 'editor',  # 图片保存文件夹名称  
    'theme': 'default',  # 编辑框主题 ，dark / default  
    'preview_theme': 'default',  # 预览区域主题， dark / default  
    'editor_theme': 'default',  # edit区域主题，pastel-on-dark / default  
    'toolbar_autofixed': True,  # 工具栏是否吸顶  
    'search_replace': True,  # 是否开启查找替换   
    'emoji': True,  # 是否开启表情功能  
    'tex': True,  # 是否开启 tex 图表功能  
    'flow_chart': True,  # 是否开启流程图功能  
    'sequence': True,  # 是否开启序列图功能  
    'watch': True,  # 实时预览  
    'lineWrapping': True,  # 自动换行  
    'lineNumbers': False  # 行号  
    }  
}  
MESSAGE_TAGS = {
    messages.INFO: 'alert alert-info',
    messages.SUCCESS: 'alert alert-success',
    messages.WARNING: 'alert alert-warning',
    messages.ERROR: 'alert alert-danger',
}

if not DEBUG:
    SECRET_KEY = os.environ['SECRET_KEY']
    import django_heroku #追加
    django_heroku.settings(locals()) #追加
    import cloudinary #追加
    cloudinary.config( 
        cloud_name = "hpeqmnspv", #追加
        api_key = os.environ['CLOUDINARY_API_KEY'], #追加  
        api_secret = os.environ['CLOUDINARY_API_SECRET'] #追加
    )
    # DB
    import dj_database_url
    db_from_env = dj_database_url.config(conn_max_age=600, ssl_require=True)
    DATABASES['default'].update(db_from_env)

