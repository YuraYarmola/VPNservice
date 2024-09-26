from django.contrib.auth.models import User
from django.db import models


class Site(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sites")
    name = models.CharField(max_length=255)
    url = models.URLField()
    transitions_count = models.IntegerField(default=0)
    data_sent = models.FloatField(default=0.0)
    data_received = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
