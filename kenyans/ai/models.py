from django.db import models
from django.utils.text import slugify

# Create your models here.
class Articles(models.Model):
    title = models.CharField(max_length=128)
    body = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=64, default='Victor Kimani')
    image_url = models.URLField(blank=True)
    link = models.SlugField(max_length=64, blank=True)

    def __str__(self):
        return f"{self.title}: {self.body} posted at {self.time}"
    
    def save(self, *args, **kwargs):
        if not self.link:
            self.link = slugify(self.title)
        super().save(*args, **kwargs)

        # After saving, call the management command to update the JSON file
        from django.core.management import call_command
        call_command('export_articles')

    