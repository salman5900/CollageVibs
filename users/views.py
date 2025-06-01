from django.shortcuts import render,redirect
from .forms import CustomUserSignupForm, CustomUserLoginForm, ProfileEditForm
from django.contrib.auth import login,logout
from .models import Profile
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .models import Profile

def register_view(request):
    if request.method == 'POST':
        form = CustomUserSignupForm(request.POST, request.FILES)  # handle file upload
        if form.is_valid():
            # Save the User part
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user = form.save()

            # Save the Profile part
            college_id = form.cleaned_data.get('college_id')
            profile_picture = form.cleaned_data.get('profile_picture')


            Profile.objects.create(
                user=user,
                college_id=college_id,
                profile_picture=profile_picture
            )

            # Log the user in
            login(request, user)
            return redirect('main:home')
    else:
        form = CustomUserSignupForm()

    return render(request, 'users/register.html', {
        'hide_navbar': True,
        'form': form
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('main:home')
    if request.method == 'POST':
        form = CustomUserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main:home')
    else:
        form = CustomUserLoginForm()
    return render(request, 'users/login.html',
{
    'hide_navbar': True,
    'form': form
})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('users:login')

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    return render(request, 'users/profile.html', {
        'profile': profile,
    })
@login_required
def profile_edit_view(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Update Profile fields
            profile = form.save(commit=False)
            profile.save()

            # Update User fields
            request.user.first_name = form.cleaned_data.get('first_name')
            request.user.last_name = form.cleaned_data.get('last_name')
            request.user.save()

            return redirect('users:profile')
    else:
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'college_id': profile.college_id,
            'profile_picture': profile.profile_picture,
        }
        form = ProfileEditForm(initial=initial_data, instance=profile)

    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def search_view(request):
    profiles = Profile.objects.select_related('user').all()
    query = request.GET.get('q')
    if query:
        profiles = profiles.filter(user__username__icontains=query)
    profiles = profiles.exclude(user=request.user)
    return render(request, 'users/search.html', {'profiles': profiles})