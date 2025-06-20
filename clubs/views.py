from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponseForbidden
from .models import Club, ClubMessage, ClubInvite
from django.contrib.auth.models import User
from .forms import ClubCreateForm 
from django.contrib.auth.decorators import login_required
from clubs.utils import notify_club_disbanded, notify_member_left
from django.contrib import messages

# Create your views here.
def club_chat(request, club_id):
    club = get_object_or_404(Club, id=club_id)

    if request.user not in club.members.all():
        return HttpResponseForbidden()
    
    message = ClubMessage.objects.filter(club=club).order_by('timestamp')

    content = {
        'club': club,
        'messages': message,
    }

    return render(request, 'clubs/club_chat.html', content)

def create_club(request):
    if request.method == 'POST':
        form = ClubCreateForm(request.POST)
        if form.is_valid():
            club = form.save(commit=False)
            club.admin = request.user  
            club.save()                
            club.members.add(request.user)
            return redirect('clubs:club_chat', club_id=club.id)
    else:
        form = ClubCreateForm()

    return render(request, 'clubs/create_club.html', {'form': form})


@login_required
def send_invite(request, club_id, user_id):
    club = get_object_or_404(Club, id=club_id)
    to_user = get_object_or_404(User, id=user_id)

    # Only creator can invite
    if request.user != club.admin:
        return HttpResponseForbidden()

    ClubInvite.objects.get_or_create(from_user=request.user, to_user=to_user, club=club)
    return redirect('users:search')  # or return JsonResponse

@login_required
def respond_invite(request, invite_id, response):
    invite = get_object_or_404(ClubInvite, id=invite_id, to_user=request.user)

    if response == 'accept':
        invite.status = 'accepted'
        invite.club.members.add(request.user)
    else:
        invite.status = 'declined'
    invite.save()
    return redirect('clubs:notifications') 

@login_required
def notifications(request):
    invites = ClubInvite.objects.filter(to_user=request.user, status='pending')
    return render(request, 'clubs/notifications.html', {'invites': invites})


@login_required
def leave_club(request, club_id):
    club = get_object_or_404(Club, id=club_id)

    if not club.members.filter(id=request.user.id).exists() and club.admin != request.user:
        return HttpResponseForbidden("You are not in this club.")
    
    if club.admin == request.user:

        club_name = club.name  # for notification
        member_ids = list(club.members.values_list('id', flat=True))  # store to notify before delete

        club.delete()  # delete the club
        notify_club_disbanded(club_name, member_ids)

    else:
        # Regular member leaves
        club.members.remove(request.user)
        notify_member_left(club, request.user)

    return redirect('main:home')



@login_required
def remove_member(request, club_id, user_id):
    club = get_object_or_404(Club, id=club_id)
    user_to_remove = get_object_or_404(User, id=user_id)

    #  Only admin can remove, and not themselves
    if request.user == club.admin and user_to_remove != request.user:
        if user_to_remove in club.members.all():
            club.members.remove(user_to_remove)
            messages.success(request, f"{user_to_remove.first_name} was removed from the club.")
        else:
            messages.error(request, "User is not a member of this club.")
    else:
        messages.error(request, "You don't have permission to do that.")

    return redirect('clubs:club_chat', club_id=club.id)
