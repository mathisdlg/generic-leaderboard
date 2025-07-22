from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.urls import reverse
from leaderboard.models import Leaderboard
from django.contrib.auth import logout as auth_logout


def create_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        conf_password = request.POST.get('confirm_password')

        if not username or not password:
            return render(request, 'error/invalid_input.html', {'message': 'Username and password are required'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'error/invalid_input.html', {'message': 'Username already exists'})

        if password != conf_password:
            return render(request, 'error/invalid_input.html', {'message': 'Passwords do not match'})        
        
        
        user = User.objects.create_user(username=username, password=password)
        user.save()
        # Automatically log in the user after creation
        login(request, user)
        # go to main page
        return redirect(reverse('main'))

    return render(request, 'registration/create_user.html')


def profile_view(request):
    if not request.user.is_authenticated:
        return render(request, 'error/auth_req.html')

    user = request.user
    leaderboards = Leaderboard.objects.filter(creator=user) | Leaderboard.objects.filter(shared_with_users=user)
    leaderboards = leaderboards.distinct().order_by('-id')

    return render(request, 'accounts/profile.html', {
        'user': user,
        'leaderboards': leaderboards,
    })
    
def edit_profile(request):
    if not request.user.is_authenticated:
        return render(request, 'error/auth_req.html')

    user = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        if username:
            user.username = username
        if email:
            user.email = email
        user.save()
        return redirect(reverse('profile'))

    return render(request, 'accounts/edit_profile.html', {'user': user})

def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect(reverse('main'))