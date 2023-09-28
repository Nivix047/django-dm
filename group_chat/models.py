from django.db import models
from users.models import CustomUser


class Group(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(CustomUser)


class GroupInvitation(models.Model):
    sender = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="sent_group_invitations")
    recipient = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="received_group_invitations")
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)


class GroupMessage(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
