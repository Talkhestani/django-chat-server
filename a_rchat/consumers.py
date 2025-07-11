from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from a_rchat.models import ChatGroup, GroupMessage
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
import json


class ChatRoomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope.get('user')
        self.chatroom_name = self.scope['url_route']['kwargs']['room_name']
        self.chatroom = get_object_or_404(ChatGroup, name=self.chatroom_name)
        
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name, self.channel_name
        )

        if self.user not in self.chatroom.users_online.all():
            self.chatroom.users_online.add(self.user)
            self.update_online_count()
        
        self.accept()


    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name, self.channel_name
        )

        if self.user in self.chatroom.users_online.all():
            self.chatroom.users_online.remove(self.user)
            self.update_online_count()
        


    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        body = text_data_json.get('body', '')
        
        message = GroupMessage.objects.create(
            group=self.chatroom,
            author=self.user,
            body=body
        )

        event = {
            'type': 'message_handler',
            'message_id': message.id
        }

        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )

    
    def message_handler(self, event):
        message_id = event['message_id']

        message = GroupMessage.objects.get(id=message_id)

        html = render_to_string(
            'a_rchat/partials/chat_message_p.html',
            context={
                'user': self.user,
                'message': message
            }
        )

        self.send(text_data=html)
    
    def update_online_count(self):
        online_count = self.chatroom.users_online.count() - 1
        event = {
            'type': 'online_count_handler',
            'online_count': online_count
        }
        async_to_sync(self.channel_layer.group_send)(self.chatroom_name, event)
    
    def online_count_handler(self, event):
        online_count = event['online_count']
        html = render_to_string(
            'a_rchat/partials/online_count.html',
            {
                'online_count': online_count,
                'chat_group': self.chatroom
            }
        )

        self.send(html)
