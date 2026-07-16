from django.db import models

# Create your models here.
from django.conf import settings
from videos.models import Video

class WatchHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    watched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-watched_at']
        unique_together = ['user', 'video']

    def __str__(self):
        return f"{self.user.username} a regardé {self.video.title}"
