from django.db import models
from django.contrib.auth.models import User


class GlobalChatStatus(models.Model):
    user_online = models.ManyToManyField(User, related_name='global_online_users', blank=True)

    def __str__(self):
        return "Global Chat Online Status"

class GlobalChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username}: {self.message[:20]}..."
    
    class Meta:
        ordering = ['-timestamp']