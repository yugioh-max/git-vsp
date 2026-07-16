from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    channel_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    
    def __str__(self):
        return f"Profil de {self.user.username}"
    
    @property
    def subscribers_count(self):
        """Calculé dynamiquement depuis la table subscriptions"""
        return self.user.subscribers.count()  
