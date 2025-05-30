from django.shortcuts import render

# Create your views here.
def noticeboard_view(request):
    return render(request, "noticeboard/noticeboardHome.html")