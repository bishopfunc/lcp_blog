from django.db import models
from django.utils.text import slugify
from mdeditor.fields import MDTextField
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=100)
    # image = models.ImageField(upload_to='media/', blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, blank=False, null=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False, blank=False, null=False)    
    body = MDTextField(blank=True, null=False)
    slug = models.SlugField(max_length=255, null=False, blank=False, unique=True, verbose_name='url')
    auther = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Post,self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:30]