from django.shortcuts import render,redirect
from .models import Noticeboard
from .forms import NoticeboardForm

def noticeboard_view(request):
    notices = Noticeboard.objects.all().order_by('-created_at')
    return render(request, "noticeboard/noticeboardHome.html", {"notices": notices})

def add_Notice(request):
    if request.method == "POST":
        form = NoticeboardForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("noticeboard:main")
    else:
        form = NoticeboardForm()

    return render(request, "noticeboard/addNotice.html", {"form": form})
