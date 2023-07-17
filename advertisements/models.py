# models.py
from django.db import models

class Ad(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    photos = models.JSONField()
    phone = models.CharField(max_length=20)
    author = models.CharField(max_length=50)

    def __str__(self):
        return self.title
