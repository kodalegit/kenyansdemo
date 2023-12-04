from django.db import models

# Create your models here.
class Articles(models.Model):
    title = models.CharField(max_length=128)
    body = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}: {self.body} posted at {self.time}"
