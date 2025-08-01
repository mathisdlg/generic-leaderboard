# from datetime import datetime
# from re import findall

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
            # expr = r"^(\d+)?:?(\d{2}):(\d{2}),?(\d{1,})?$"
            # res = findall(expr,score)
            # timestamp = datetime(1970,1,1)
            # if res:
            #     days = 0
            #     hours = res[0][0]
            #     if res[0][0] and int(res[0][0]) > 23:
            #         days = int(res[0][0])//24
            #         hours = str(int(res[0][0]) % 24)
            #     timestamp = datetime(
            #         year = 1970,
            #         month = 1,
            #         day = days + 1,
            #         hour = int(hours) if hours != '' else 0,
            #         minute = int(res[0][1]),
            #         second = int(res[0][2]),
            #         microsecond = int(res[0][3])*pow(10,6-len(res[0][3])) if res[0][3] != '' else 0
            #     )
            # entry = LeaderboardEntry(user=request.user, score=timestamp)
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
