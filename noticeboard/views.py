from django.shortcuts import render,redirect
from .models import Noticeboard
from .forms import NoticeboardForm

def noticeboard_view(request):
    notices = Noticeboard.objects.all().order_by('-created_at')
    return render(request, "noticeboard/noticeboardHome.html", {"notices": notices})
def my_Notices(request):
    notices = Noticeboard.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "noticeboard/myNotices.html", {"notices": notices})
def add_Notice(request):
    if request.method == "POST":
        form = NoticeboardForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect("noticeboard:main")
    else:
        form = NoticeboardForm()

    return render(request, "noticeboard/addNotice.html", {"form": form})

def delete_Notice(request, slug):
    notice = Noticeboard.objects.get(slug=slug, user=request.user)
    notice.delete()
    return redirect("noticeboard:my_notice")

def edit_Notice(request, slug):
    notice = Noticeboard.objects.get(slug=slug, user=request.user)

    if request.method == "POST":
        form = NoticeboardForm(request.POST, request.FILES, instance=notice)
        if form.is_valid():
            form.save()
            return redirect("noticeboard:my_notice")
    else:
        form = NoticeboardForm(instance=notice)

    return render(request, "noticeboard/editNotice.html", {"form": form})


