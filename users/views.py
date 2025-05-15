from django.shortcuts import render,redirect
from .forms import CustomUserSignupForm, CustomUserLoginForm
from django.contrib.auth import login,logout
# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = CustomUserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:home')
    else:
        form = CustomUserSignupForm()
    return render(request, 'users/register.html',
    {
        'hide_navbar': True,
        'form': form
    })

def login_view(request):
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