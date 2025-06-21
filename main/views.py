from django.shortcuts import render
from clubs.models import Club
from django.contrib.auth.decorators import login_required
from .utils import get_global_online_count, get_club_online_counts
from globalchat.models import GlobalChatMessage, GlobalChatSeen
from clubs.models import ClubChatSeen, ClubMessage
from django.utils import timezone
from django.db.models import Q

@login_required
def home(request):
    clubs = Club.objects.filter(is_active=True, members=request.user).order_by('name')

    online_users_global = get_global_online_count()
    club_ids = [club.id for club in clubs]
    online_users_club = get_club_online_counts(club_ids)

    # Global chat unread (excluding messages sent by current user)
    last_seen_obj = GlobalChatSeen.objects.filter(user=request.user).first()
    if last_seen_obj:
        unread_global = GlobalChatMessage.objects.filter(
            Q(timestamp__gt=last_seen_obj.last_seen) & ~Q(user=request.user)
        ).count()
    else:
        unread_global = GlobalChatMessage.objects.exclude(user=request.user).count()

    # Club chat unread counts (excluding messages sent by current user)
    unread_club_counts = {}
    for club in clubs:
        seen_obj = ClubChatSeen.objects.filter(user=request.user, club=club).first()
        if seen_obj:
            count = ClubMessage.objects.filter(
                Q(club=club) & Q(timestamp__gt=seen_obj.last_seen) & ~Q(user=request.user)
            ).count()
        else:
            count = ClubMessage.objects.filter(club=club).exclude(user=request.user).count()
        unread_club_counts[club.id] = count

    # Assign gradient class to each club
    for i, club in enumerate(clubs):
        club.gradient_class = f"gradient-{(i % 15) + 1}"

    context = {
        'online_users_global': online_users_global,
        'clubs': clubs,
        'online_users_club': online_users_club or {},
        'unread_global': unread_global,
        'unread_club_counts': unread_club_counts,
    }

    return render(request, 'main/home.html', context)




def about(request):
    return render(request, 'main/about.html')
