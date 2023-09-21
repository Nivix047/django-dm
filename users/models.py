from django.db import models
from django.contrib.auth.models import AbstractUser

# Django automaically requires a username, email, password


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
