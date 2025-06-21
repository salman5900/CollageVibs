from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import GlobalChatMessage, GlobalChatSeen
from .forms import GlobalChatCreateForm
from django.utils import timezone

@login_required
def global_chat(request):
    # Get last seen time BEFORE updating it
    seen_obj = GlobalChatSeen.objects.filter(user=request.user).first()
    last_seen_time = seen_obj.last_seen if seen_obj else None

    # Fetch messages (most recent last)
    global_chat_messages = list(GlobalChatMessage.objects.all().order_by('timestamp'))

    # Compute index of first unread message (excluding user's own messages)
    first_unread_index = None
    if last_seen_time:
        for i, msg in enumerate(global_chat_messages):
            if msg.timestamp > last_seen_time and msg.user != request.user:
                first_unread_index = i
                break

    # Update the last seen timestamp after computing unread
    GlobalChatSeen.objects.update_or_create(
        user=request.user,
        defaults={'last_seen': timezone.now()}
    )

    form = GlobalChatCreateForm()
    context = {
        'global_chat_messages': global_chat_messages,
        'form': form,
        'first_unread_index': first_unread_index,
    }

    return render(request, 'globalchat/global_chat.html', context)
