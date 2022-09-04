from django.db import models
from django.utils.text import slugify
from mdeditor.fields import MDTextField
from django.contrib.auth.models import User
from datetime import datetime
import pykakasi
from cloudinary.models import CloudinaryField

class Category(models.Model):
    name = models.CharField('カテゴリー', max_length=50)
    text = models.CharField('説明', max_length=100, blank=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'CATEGORY'


class Tag(models.Model):
    name = models.CharField('タグ', max_length=50)
    text = models.CharField('説明', max_length=100, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'TAGS'

FONT_CHOICES = (
    (1, 'Noto Serif SC'),
    (2, 'EB Garamond'),
    (3, 'Shippori Mincho'),
)


class Post(models.Model):
    title = models.CharField(max_length=100)
    image = CloudinaryField('image', folder='media/', blank=True, null=False)
    created_at = models.DateTimeField(default=datetime.now, editable=True, blank=False, null=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False, blank=False, null=False)    
    body = MDTextField(blank=True, null=False)
    slug = models.SlugField(max_length=255, null=False, blank=True, unique=True, verbose_name='url')
    auther = models.ForeignKey('auth.User', on_delete=models.PROTECT, default=1)
    category = models.ForeignKey(Category, verbose_name='Category', on_delete=models.PROTECT, blank=True, null=True, unique=True)
    tags = models.ManyToManyField(Tag, verbose_name='Tag', blank=True, null=True, related_name='posts')
    relation = models.ManyToManyField('self', verbose_name='関連記事', blank=True, null=True)
    font = models.IntegerField(choices=FONT_CHOICES, blank=True, null=True)
    draft_flg = models.BooleanField(default=False, blank=False, null=False, verbose_name='下書きで保存')

    class Meta:
        verbose_name_plural = 'BLOG'

    def save(self, *args, **kwargs):
        # slugがないときはローマ字を元に自動生成
        if not self.slug:
            kks = pykakasi.kakasi()
            title = self.title
            kks_dict = kks.convert(title)
            r_title = ''
            for kks in kks_dict:
                r_title += kks['passport']
            self.slug = slugify(r_title)
        return super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:30]