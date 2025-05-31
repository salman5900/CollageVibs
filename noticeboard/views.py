from django.shortcuts import render
from .models import Noticeboard

def noticeboard_view(request):
    notices = Noticeboard.objects.all().order_by('-created_at')
    return render(request, "noticeboard/noticeboardHome.html", {"notices": notices})
