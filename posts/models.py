from django.db import models
from django.utils.text import slugify
from mdeditor.fields import MDTextField
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField('カテゴリー', max_length=50)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'CATEGORY'


class Tag(models.Model):
    name = models.CharField('タグ', max_length=50)

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
    # image = models.ImageField(upload_to='media/', blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, blank=False, null=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False, blank=False, null=False)    
    body = MDTextField(blank=True, null=False)
    slug = models.SlugField(max_length=255, null=False, blank=False, unique=True, verbose_name='url')
    auther = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    category = models.ForeignKey(Category, verbose_name='Category', on_delete=models.PROTECT, blank=True, null=True, unique=True)
    tag = models.ManyToManyField(Tag, verbose_name='Tag', blank=True, null=True)
    relation = models.ManyToManyField('self', verbose_name='関連記事', blank=True, null=True)
    font = models.IntegerField(choices=FONT_CHOICES, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'BLOG'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        # tags = Tag.objects.all()
        # instance = Post.objects.create(name = tags.name)
        # instance.tag.add(*tags)
        return super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:30]