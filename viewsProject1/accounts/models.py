from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    GENDER_CHOICE = (
        ('male', '남성'),
        ('female', '여성'),
        ('other', '중성'),
    )

    birthday = models.DateField()
    gender = models.TextField(max_length=6, choices=GENDER_CHOICE)
    incroduction = models.TextField(max_length=100, blank=True, null=True)