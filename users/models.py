from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college_id = models.PositiveIntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(9999)],
        help_text="4 digit college ID",
    )
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True,default='profile_pictures/default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
