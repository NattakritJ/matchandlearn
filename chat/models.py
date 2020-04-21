from django.db import models


# store chat log of all user
class ChatLog(models.Model):
    name = models.TextField(blank=True)
    partner_username = models.TextField(blank=True)
    your_username = models.TextField(blank=True)
    chat = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
