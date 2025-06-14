from django.shortcuts import render
from globalchat.models import GlobalChatStatus
from clubs.models import Club, ClubMessage, ClubInvite, ClubChatStatus
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    # Global online count
    online_users_global = GlobalChatStatus.objects.first().user_online.count() if GlobalChatStatus.objects.exists() else 0

    # Active clubs the user is part of
    clubs = Club.objects.filter(is_active=True, members=request.user).order_by('name')

    # Per club online user count
    statuses = ClubChatStatus.objects.filter(club__in=clubs).prefetch_related('user_online')
    online_users_club = {status.club.id: status.user_online.count() for status in statuses}

    for i, club in enumerate(clubs):
        club.gradient_class = f"gradient-{(i % 15) + 1}"

    context = {
        'online_users_global': online_users_global,
        'clubs': clubs,
        "online_users_club": online_users_club or {},
    }

    return render(request, 'main/home.html', context)
