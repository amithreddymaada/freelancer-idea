from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Requirement(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    content=models.TextField()
    datecreated=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Requirement of {self.title}'
    
