from django.shortcuts import render
from globalchat.models import GlobalChatStatus
from clubs.models import Club, ClubChatStatus
from django.contrib.auth.decorators import login_required
from .utils import get_global_online_count, get_club_online_counts

@login_required
def home(request):
    # Get user clubs
    clubs = Club.objects.filter(is_active=True, members=request.user).order_by('name')

    # Redis-based global count
    online_users_global = get_global_online_count()

    # Redis-based per-club online counts
    club_ids = [club.id for club in clubs]
    online_users_club = get_club_online_counts(club_ids)

    # Add gradient class for UI
    for i, club in enumerate(clubs):
        club.gradient_class = f"gradient-{(i % 15) + 1}"

    context = {
        'online_users_global': online_users_global,
        'clubs': clubs,
        "online_users_club": online_users_club or {},
    }

    return render(request, 'main/home.html', context)


def about(request):
    return render(request, 'main/about.html')
