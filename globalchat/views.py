from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import GlobalChatMessage, GlobalChatSeen
from .forms import GlobalChatCreateForm
from django.utils import timezone

@login_required
def global_chat(request):
    # Update last seen for this user
    GlobalChatSeen.objects.update_or_create(
        user=request.user,
        defaults={'last_seen': timezone.now()}
    )

    # Last 30 messages (newest at bottom)
    global_chat_messages = list(GlobalChatMessage.objects.all().order_by('-timestamp'))

    form = GlobalChatCreateForm()
    context = {
        'global_chat_messages': global_chat_messages,
        'form': form,
    }
    return render(request, 'globalchat/global_chat.html', context)
