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