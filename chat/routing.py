from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<user1>\w+)/(?P<user2>\w+)/$', consumers.ChatConsumer),
    re_path(r'ws/freelancer/room/(?P<room_name>\w+)/$', consumers.FreelancerRoomConsumer),
    re_path(r'ws/freelancer/chat/(?P<room_name>\w+)/$', consumers.FreelancerChatConsumer),
]