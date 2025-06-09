from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponseForbidden
from .models import Club
from .forms import ClubCreateForm 

# Create your views here.
def club_chat(request, club_id):
    club = get_object_or_404(Club, id=club_id)

    if request.user not in club.members.all():
        return HttpResponseForbidden()

    return render(request, 'clubs/club_chat.html', {'club': club})

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
