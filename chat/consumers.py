import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.models import Message,Room,FreelancerChat,OnGoingProjects
from django.contrib.auth.models import User
from django.utils import timezone

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user1 = self.scope['url_route']['kwargs']['user1']
        self.user2 = self.scope['url_route']['kwargs']['user2']
        self.author=self.user1
        #to sort the two usernames and find the first one based upon we create a chat between that two users
        users=[self.user1,self.user2]
        users=sorted(users)

        self.user1=users[0]
        self.user2=users[1]

        self.room_name=f'{self.user1}_{self.user2}'
        self.room_group_name = f'chat_{self.user1}_{self.user2}'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self,data)

    def fetch_messages(self,data):
        messages=Message.objects.filter(sort_str=f'{self.user1}_{self.user2}')
        context = {
            'command':'messages',
            'messages':self.messages_to_json(messages)
        }
        self.send_messages(context)
        

    def new_messsage(self,data):
        msg_data=data
        # user=self.scope['user']
        # print(user.username)
        
        user=User.objects.get(username=self.author)
        message=Message.objects.create(author=user,sort_str=f'{self.user1}_{self.user2}',content=msg_data['message'])
        context={
            'command':'new_message',
            'message':self.message_to_json(message)
        }
        self.send_chat_messages(context)

    commands={
        'fetch_messages':fetch_messages,
        'new_message':new_messsage
    }

    def messages_to_json(self,messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result
    def message_to_json(self,message):
        return(
                {
                    'author':message.author.username,
                    'content':message.content,
                    'timestamp':str(message.timestamp)
                }
            )
    
    def send_messages(self,messages):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'previous_chats',
                'messages': messages
            }
        )
    def previous_chats(self,event):
        messages = event['messages']
        self.send(text_data=json.dumps(messages))

    def send_chat_messages(self,context):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'context': context
            }
        )
        # print('at the end of send_chat_messages')
        # self.send(text_data=json.dumps({
        #     'message': context['message'],
        #     'command':context['command']
        # }))
        

    # Receive message from room group
    def chat_message(self, event):
        context = event['context']
        # print(context['message'])
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': context['message'],
            'command':context['command']
        }))














#---------------------------------------------------------------------------------
#this is consumer of the room chat of the freelancing website 

class FreelancerRoomConsumer(WebsocketConsumer):
    def fetch_messages(self,data):
        messages=Room.objects.filter(room_name=self.room_name).all()
        context = {
            'command':'messages',
            'messages':self.messages_to_json(messages)
        }
        self.send_messages(context)
        

    def new_messsage(self,data):
        msg_data=data
        user=self.scope['user']
        print(user.username)
        user=User.objects.filter(username=user.username)[0]
        message=Room.objects.create(author=user,room_name=self.room_name,content=msg_data['message'])
        context={
            'command':'new_message',
            'message':self.message_to_json(message)
        }
        self.send_chat_messages(context)

    commands={
        'fetch_messages':fetch_messages,
        'new_message':new_messsage
    }

    def messages_to_json(self,messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result
    def message_to_json(self,message):
        return(
                {
                    'author':message.author.username,
                    'content':message.content,
                    'timestamp':str(message.timestamp)
                }
            )

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self,data)
    
    def send_messages(self,messages):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'previous_chats',
                'messages': messages
            }
        )
    def previous_chats(self,event):
        messages = event['messages']
        self.send(text_data=json.dumps(messages))

    def send_chat_messages(self,context):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'context': context
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        context = event['context']
        print(context['message'])
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': context['message'],
            'command':context['command']
        }))


















class FreelancerChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.author=self.scope['user'].username
        
        self.room_group_name = f'freelancer_chat_{self.room_name}'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self,data)

    def fetch_messages(self,data):
        messages=FreelancerChat.objects.filter(room_name=self.room_name)
        context = {
            'command':'messages',
            'messages':self.messages_to_json(messages)
        }
        self.send_messages(context)
        

    def new_messsage(self,data):
        msg_data=data
        user=User.objects.get(username=self.author)
        message=FreelancerChat.objects.create(author=user,room_name=self.room_name,content=msg_data['message'])
        context={
            'command':'new_message',
            'message':self.message_to_json(message)
        }
        self.send_chat_messages(context)

    commands={
        'fetch_messages':fetch_messages,
        'new_message':new_messsage
    }

    def messages_to_json(self,messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result
    def message_to_json(self,message):
        return(
                {
                    'author':message.author.username,
                    'content':message.content,
                    'timestamp':str(message.timestamp)
                }
            )
    
    def send_messages(self,messages):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'previous_chats',
                'messages': messages
            }
        )
    def previous_chats(self,event):
        messages = event['messages']
        self.send(text_data=json.dumps(messages))

    def send_chat_messages(self,context):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'context': context
            }
        )
        
    def chat_message(self, event):
        context = event['context']
        # print(context['message'])
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': context['message'],
            'command':context['command']
        }))
