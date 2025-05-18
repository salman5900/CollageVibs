from django.shortcuts import render

# Create your views here.
def global_chat(request):
    return render(request, 'globalchat/global_chat.html')