from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Message(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    sort_str=models.CharField(max_length=100)
    content=models.TextField()
    timestamp=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.content} by {self.author} in {self.sort_str}'

    def retrive_messages():
        return reversed(Message.objects.order_by('-timestamp').all())

class Room(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    room_name=models.CharField(max_length=50)
    content=models.TextField()
    timestamp=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.content} by {self.author} in room:{self.room_name}'

class FreelancerChat(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    room_name=models.CharField(max_length=50,default='')
    content=models.TextField()
    timestamp=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.content} by {self.author} in freelancer chat of{self.room_name}'

    
    
class OnGoingProjects(models.Model):
    provider=models.ForeignKey(User,related_name='provider_set',on_delete=models.CASCADE)
    performer=models.ForeignKey(User,related_name='performer_set',on_delete=models.CASCADE)
    room_name=models.CharField(max_length=50)

    def __str__(self):
        return f'{self.room_name} chat between {self.provider} and {self.performer}'

    

