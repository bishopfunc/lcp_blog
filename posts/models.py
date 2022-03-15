from django.db import models
from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/', blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, blank=False, null=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False, blank=False, null=False)    
    body = models.TextField(blank=True, null=False)
    slug = models.SlugField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Post,self).save(*args, **kwargs)


    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:30]