from django.shortcuts import render, redirect
from leaderboard.models import Leaderboard, LeaderboardEntry, RealiseWith
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def add_entry(request, leaderboard_id):
    leaderboard = Leaderboard.objects.get(id=leaderboard_id)
    if not leaderboard.have_access(request.user):
        return render(request, 'error/auth_req.html')
    
    if request.method == "POST":
        name = request.POST.get('name')
        score = request.POST.get('value')
        option_ids = request.POST.getlist('options', [])

        if name:
            entry = LeaderboardEntry(name=name, score=score, realise_with=RealiseWith.objects.filter(id__in=option_ids))
            entry.save()
            leaderboard.entries.add(entry)
            return redirect('leaderboard_detail', leaderboard_id=leaderboard.id)

    return render(request, "leaderboard/entries/add_entry.html", {"leaderboard": leaderboard})