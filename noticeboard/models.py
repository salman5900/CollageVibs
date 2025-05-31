from django.db import models
from django.utils.text import slugify
import uuid

class Noticeboard(models.Model): 
    title = models.CharField(max_length=200) 
    slug = models.SlugField(unique=True, blank=True) 
    image = models.ImageField(blank=True, null=True) 
    content = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
 
    def __str__(self): 
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_id = uuid.uuid4().hex[:6]
            self.slug = f"{base_slug}-{unique_id}"
        super().save(*args, **kwargs)