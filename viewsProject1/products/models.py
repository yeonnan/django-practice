from django.db import models
from django.conf import settings


class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    context = models.TextField()
    image = models.ImageField(null=True, blank=True)