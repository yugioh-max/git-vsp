from django.db import models

# Create your models here.
from django.conf import settings

class Subscription(models.Model):
    subscriber = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions'  # user.subscriptions.all() → créateurs suivis
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscribers'  # user.subscribers.all() → abonnés
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['subscriber', 'creator']

    def __str__(self):
        return f"{self.subscriber.username} s'abonne à {self.creator.username}"

