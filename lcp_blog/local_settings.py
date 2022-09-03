import os
import cloudinary

DEBUG = True #ローカルでDebugできるようになります
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
SECRET_KEY = 'u&3nsb&bp76%d@xsb*ehh&g(f$7v^42=v=)aq9w+(nig3byk=j'


cloudinary.config( 
  cloud_name = "hpeqmnspv", 
  api_key = "739416666445432", 
  api_secret = "nNNWoDv4uwTmAEudxaUXsRIVHEE" 
) # 追加