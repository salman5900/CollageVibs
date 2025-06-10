from django.db import models
from django.contrib.auth.models import User

class Club(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_clubs')
    members = models.ManyToManyField(User, related_name='clubs', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class ClubMessage(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}: {self.message[:20]}..."

    class Meta:
        ordering = ['-timestamp']

class ClubInvite(models.Model):
    from_user = models.ForeignKey(User, related_name="sent_invites", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="received_invites", on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')], default='pending')



class ClubChatStatus(models.Model):
    club = models.OneToOneField('Club', on_delete=models.CASCADE)
    user_online = models.ManyToManyField(User, blank=True)
