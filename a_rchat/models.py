from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ChatGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)
    users_online = models.ManyToManyField(User, related_name='online_in_groups', blank=True)

    def __str__(self):
        return self.name


class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author}: {self.body[:20]}..."
    
    class Meta:
        ordering = ['-created']
        verbose_name = 'Group Message'
        verbose_name_plural = 'Group Messages'
