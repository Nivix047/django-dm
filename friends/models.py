from django.db import models
from django.conf import settings

class FriendRequest(models.Model):
  sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_requests', on_delete=models.CASCADE)
  receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_requests', on_delete=models.CASCADE)
  timestamp = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = (('sender', 'receiver'),)

class FriendList(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='friend_list', on_delete=models.CASCADE)
  friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

  def add_friend(self, account):
    """
    Add a new friend.
    """
    self.friends.add(account)

  def remove_friend(self, account):
    """
    Remove a friend.
    """
    self.friends.remove(account)  
