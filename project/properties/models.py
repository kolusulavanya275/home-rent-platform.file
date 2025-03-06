# models.py
from django.db import models

class MyModel(models.Model):
    name = models.TextField(max_length=100)
    details = models.TextField()
    new_field = models.TextField(max_length=100, null=True)  # New field added

    def __str__(self):
        return self.name

