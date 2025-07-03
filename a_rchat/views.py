from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from a_rchat.forms import GroupMessageForm
from a_rchat.models import GroupMessage, ChatGroup


# Create your views here.
@login_required
def chat_view(request):
    messages = GroupMessage.objects.filter(group__name='public-chat')
    form = GroupMessageForm()
    
    if request.htmx:
        form = GroupMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = ChatGroup.objects.get(name='public-chat')
            message.save()
            return render(request, 'a_rchat/chat_messages.html', {'message': message})
    
    context = {
        'messages': messages,
        'form': form,
    }
    return render(request, template_name='a_rchat/chat.html', context=context)
