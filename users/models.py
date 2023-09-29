from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
from rest_framework.authtoken.models import Token as DefaultToken

# Django automaically requires a username, email, password


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)


class ValidTokenManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(expiration_time__gt=timezone.now())


class ExpiringToken(DefaultToken):
    expiration_time = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Set the expiration time to 24 hours after token creation
        self.expiration_time = timezone.now() + timedelta(hours=24)
        super(ExpiringToken, self).save(*args, **kwargs)

    objects = models.Manager()
    valid_tokens = ValidTokenManager()
