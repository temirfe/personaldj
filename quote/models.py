from django.db import models

# Create your models here.
class Quote(models.Model):
    body = models.CharField(max_length=500)
    author = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.body