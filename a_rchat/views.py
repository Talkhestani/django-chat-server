from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from a_rchat.forms import GroupMessageForm, NewGroupFrom
from a_rchat.models import GroupMessage, ChatGroup


# Create your views here.
@login_required
def chat_view(request, chatroom_name='public-chat'):
    chat_group = get_object_or_404(ChatGroup, name=chatroom_name)
    chat_messages = GroupMessage.objects.filter(group__name=chatroom_name)
    form = GroupMessageForm()
    
    other_user = None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404()
        for member in chat_group.members.all():
            if member != request.user:
                other_user = member
                break


    if chat_group.chat_name:
        if request.user not in chat_group.members.all():
            chat_group.members.add(request.user)


    if request.htmx:
        form = GroupMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            return render(request, 'a_rchat/chat_messages.html', {'message': message})
    
    context = {
        'messages': chat_messages,
        'form': form,
        'other_user': other_user,
        'chatroom_name': chatroom_name,
        'chat_group': chat_group
    }
    return render(request, template_name='a_rchat/chat.html', context=context)


@login_required
def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect('home')

    other_user = get_object_or_404(User, username=username)

    my_chatrooms = request.user.chat_groups.filter(is_private=True)
    chatroom = None
    for room in my_chatrooms:
        if room.members.filter(id=other_user.id).exists():
            chatroom = room
            break

    if not chatroom:
        chatroom = ChatGroup.objects.create(is_private=True)
        chatroom.members.add(request.user, other_user)

    return redirect('a_rchat:chatroom', chatroom.name)


@login_required
def create_group(request):
    form = NewGroupFrom()
    
    if request.method == 'POST':
        form = NewGroupFrom(request.POST)
        if form.is_valid():
            new_group = form.save(commit=False)
            new_group.admin = request.user
            new_group.save()
            new_group.members.add(request.user)
            return redirect('a_rchat:chatroom', new_group.name)
    
    return render(
        request,
        template_name='a_rchat/create_group.html',
        context={
            'form': form
        }
    )