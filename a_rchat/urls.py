from django.urls import path
from .views import chat_view, get_or_create_chatroom, create_group

app_name = 'a_rchat'
urlpatterns = [
    path('', chat_view, name='home'),
    path('chat/room/<chatroom_name>/', chat_view, name='chatroom'),
    path('chat/new_group/', create_group, name='new-group'),
    path('chat/<username>/', get_or_create_chatroom, name='start-chat'),
]
