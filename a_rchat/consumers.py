from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from a_rchat.models import ChatGroup, GroupMessage
from django.template.loader import render_to_string
import json


class ChatRoomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope.get('user')
        self.chatroom_name = self.scope['url_route']['kwargs']['room_name']
        self.chatroom = get_object_or_404(ChatGroup, name=self.chatroom_name)
        self.accept()
    
    
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        body = text_data_json.get('body', '')
        
        message = GroupMessage.objects.create(
            group=self.chatroom,
            author=self.user,
            body=body
        )

        html = render_to_string(
            'a_rchat/partials/chat_message_p.html',
            context={
                'user': self.user,
                'message': message
            }
        )
        self.send(text_data=html)
