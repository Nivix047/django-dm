from django.db import models
from users.models import CustomUser

class CustomMessage(models.Model):  
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE, null=True, blank=True)
    recipient = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
