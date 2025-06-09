from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import GlobalChatMessage
from .forms import GlobalChatCreateForm

@login_required
def global_chat(request):
    global_chat_messages = GlobalChatMessage.objects.all()[:30]

    form = GlobalChatCreateForm()
    context = {
        'global_chat_messages': global_chat_messages,
        'form': form,
    }
    return render(request, 'globalchat/global_chat.html', context)

