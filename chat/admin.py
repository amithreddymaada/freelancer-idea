from django.contrib import admin
from .models import Message,Room,OnGoingProjects,FreelancerChat

admin.site.register(Message)
admin.site.register(Room)
admin.site.register(OnGoingProjects)
admin.site.register(FreelancerChat)
