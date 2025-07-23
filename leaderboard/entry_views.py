from django.shortcuts import render, redirect
from leaderboard.models import Leaderboard, LeaderboardEntry, RealiseWith
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def add_entry(request, leaderboard_id):
    leaderboard = Leaderboard.objects.get(id=leaderboard_id)
    if not leaderboard.have_access(request.user):
        return render(request, 'error/auth_req.html')
    options = RealiseWith.objects.filter(belongs_to=leaderboard)
    
    if request.method == "POST":
        score = request.POST.get('value')
        option_ids = request.POST.get('realise_with_options', '').split(',')
        if option_ids == ['']:
            option_ids = []

        if score:
            entry = LeaderboardEntry(user=request.user, score=score)
            entry.save()
            entry.realise_with.set(RealiseWith.objects.filter(id__in=option_ids))
            leaderboard.entries.add(entry)
            return redirect('leaderboard_detail', leaderboard_id=leaderboard.id)

    return render(request, "leaderboard/entries/add_entry.html", {"leaderboard": leaderboard, "options": options})

@login_required
def delete_entry(request, leaderboard_id, entry_id):
    try:
        leaderboard = Leaderboard.objects.get(id=leaderboard_id, creator=request.user)
        entry = LeaderboardEntry.objects.get(id=entry_id, user=request.user)
    except (Leaderboard.DoesNotExist, LeaderboardEntry.DoesNotExist):
        return render(request, 'error/404.html', status=404, context={'message': 'Leaderboard or entry not found or you do not have permission to delete it'})

    if request.method == 'POST':
        entry.delete()
        return redirect('leaderboard_detail', leaderboard_id=leaderboard.id)

    return render(request, 'leaderboard/entries/delete_entry.html', {'entry': entry, 'leaderboard': leaderboard})