from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.
@login_required
def global_chat(request):
    global_chat_messages = GlobalChatMessage.objects.all()[:30]
    return render(request, 'globalchat/global_chat.html', {'global_chat_messages': global_chat_messages})