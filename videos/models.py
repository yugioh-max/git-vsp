from django.db import models

# Create your models here.
from django.conf import settings
from cloudinary.models import CloudinaryField

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Video(models.Model):
    VISIBILITY_CHOICES = (
        ('public', 'Public'),
        ('unlisted', 'Non répertoriée'),
        ('private', 'Privée'),
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video_file = CloudinaryField('video', resource_type='video')
    thumbnail = CloudinaryField('thumbnail', blank=True, null=True)
    
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='videos')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='videos')
    
    views_count = models.IntegerField(default=0)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
