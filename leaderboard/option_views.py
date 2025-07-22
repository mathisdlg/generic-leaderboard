from django.shortcuts import render, redirect
from leaderboard.models import Leaderboard, LeaderboardEntry, RealiseWith
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def add_option(request, leaderboard_id):
    leaderboard = Leaderboard.objects.get(id=leaderboard_id)
    if not leaderboard.have_access(request.user):
        return render(request, 'error/auth_req.html')
    
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description', None)

        if name:
            option = RealiseWith(name=name, description=description, belongs_to=leaderboard)
            option.save()
            return redirect('leaderboard_detail', leaderboard_id=leaderboard.id)

    return render(request, "leaderboard/options/add_option.html", {"leaderboard": leaderboard})

@login_required
def edit_option(request, leaderboard_id, option_id):
    leaderboard = Leaderboard.objects.get(id=leaderboard_id)
    if not leaderboard.have_access(request.user):
        return render(request, 'error/auth_req.html')

    option = RealiseWith.objects.get(id=option_id, belongs_to=leaderboard)
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description', None)

        if name:
            option.name = name
            option.description = description
            option.save()
            return redirect('leaderboard_detail', leaderboard_id=leaderboard.id)

    return render(request, "leaderboard/options/edit_option.html", {"leaderboard": leaderboard, "option": option})

@login_required
def delete_option(request, leaderboard_id, option_id):
    leaderboard = Leaderboard.objects.get(id=leaderboard_id)
    if not leaderboard.have_access(request.user):
        return render(request, 'error/auth_req.html')

    option = RealiseWith.objects.get(id=option_id, belongs_to=leaderboard)
    if request.method == "POST":
        option.delete()
        return redirect('leaderboard_detail', leaderboard_id=leaderboard.id)

    return render(request, "leaderboard/options/delete_option.html", {"leaderboard": leaderboard, "option": option})