from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import GlobalChatMessage
from .forms import GlobalChatCreateForm

@login_required
def global_chat(request):
    global_chat_messages = GlobalChatMessage.objects.all()[:30]

    if request.method == "POST" and request.htmx:
        form = GlobalChatCreateForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.user = request.user
            chat.save()
            context = {'chat': chat}
            # Return only the single chat message partial
            return render(request, 'globalchat/partials/global_chat_message.html', context)

    # Regular GET request: render the full page
    form = GlobalChatCreateForm()
    context = {
        'global_chat_messages': global_chat_messages,
        'form': form,
    }
    return render(request, 'globalchat/global_chat.html', context)
