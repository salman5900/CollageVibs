from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import GlobalChatCreateForm

# Create your views here.
@login_required
def global_chat(request):
    global_chat_messages = GlobalChatMessage.objects.all()[:30]

    if request.htmx:
        form = GlobalChatCreateForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.user = request.user
            chat.save()
            context = {
                'chat': chat,
                'user': request.user,
            }
            return render(request, 'globalchat/partials/global_chat_message_p.html', context)
    else:
        form = GlobalChatCreateForm()


    return render(request, 'globalchat/global_chat.html', {'global_chat_messages': global_chat_messages, 'form': form})