from django.shortcuts import render, redirect
from leaderboard.models import Leaderboard, LeaderboardEntry
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

def main_view(request):
    return render(request, 'main.html')

def leaderboard_list(request):
    if not request.user.is_authenticated:
        leaderboards = Leaderboard.objects.filter(public=True).order_by('-id')
    else:
        leaderboards = Leaderboard.objects.filter(
            creator=request.user
        ) | Leaderboard.objects.filter(shared_with_users=request.user) | Leaderboard.objects.filter(public=True)
    return render(request, 'leaderboard/leaderboards_list.html', {"leaderboards": leaderboards})

def leaderboard_detail(request, leaderboard_id): 
    try:
        leaderboard = Leaderboard.objects.get(id=leaderboard_id)
    except Leaderboard.DoesNotExist:
        return render(request, 'error/404.html', status=404, context={'message': 'Leaderboard not found'})
    
    print(leaderboard.public)
    if not request.user.is_authenticated and not leaderboard.public:
        return render(request, 'error/auth_req.html')

    page_number = request.GET.get('page', "1")
    if not page_number.isdigit() or int(page_number) < 1:
        page_number = 1
    nb_by_page = request.GET.get('nb_by_page', "10")
    if not nb_by_page.isdigit() or int(nb_by_page) < 1:
        nb_by_page = 10
    entries = leaderboard.get_page(page_number=int(page_number), entries_per_page=int(nb_by_page))
    nb_pages = leaderboard.get_nb_pages()

    return render(request, 'leaderboard/leaderboard_detail.html', {
        'leaderboard': leaderboard,
        'entries': entries,
        'page_number': page_number,
        'nb_pages': nb_pages,
        'nb_by_page': nb_by_page,
    })
    
@login_required
def create_leaderboard(request):
    if not request.user.is_authenticated:
        return render(request, 'error/auth_req.html')
    
    users = User.objects.all().exclude(id=request.user.id)
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', None)
        public = request.POST.get('public', 'false') == 'true'
        print(public)
        shared_with = request.POST.get('shared_with_users', "").split(",")
        if shared_with == [''] or not shared_with:
            shared_with = []
        if not name:
            return render(request, 'error/invalid_input.html', {'message': 'Name is required'})

        leaderboard = Leaderboard.objects.create(creator=request.user, name=name, description=description, public=public)
        leaderboard.shared_with_users.set(shared_with)
        return render(request, 'leaderboard/leaderboard_detail.html', {'leaderboard': leaderboard})

    return render(request, 'leaderboard/create_leaderboard.html', {'users': users})

@login_required
def edit_leaderboard(request, leaderboard_id):
    try:
        leaderboard = Leaderboard.objects.get(id=leaderboard_id, creator=request.user)
    except Leaderboard.DoesNotExist:
        return render(request, 'error/404.html', status=404, context={'message': 'Leaderboard not found or you do not have permission to edit it'})

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', None)
        public = request.POST.get('public', 'false') == 'true'
        shared_with = request.POST.get('shared_with_users', "").split(",")
        if shared_with == [''] or not shared_with:
            shared_with = []
        
        if not name:
            return render(request, 'error/invalid_input.html', {'message': 'Name is required'})
        
        leaderboard.name = name
        leaderboard.description = description
        leaderboard.public = public
        leaderboard.shared_with_users.set(shared_with)
        leaderboard.save()
        
        return redirect('leaderboard_detail', leaderboard_id=leaderboard.id)

    users = User.objects.all().exclude(id=request.user.id)
    return render(request, 'leaderboard/edit_leaderboard.html', {'leaderboard': leaderboard, 'users': users})

@login_required
def delete_leaderboard(request, leaderboard_id):
    try:
        leaderboard = Leaderboard.objects.get(id=leaderboard_id, creator=request.user)
    except Leaderboard.DoesNotExist:
        return render(request, 'error/404.html', status=404, context={'message': 'Leaderboard not found or you do not have permission to delete it'})

    if request.method == 'POST':
        leaderboard.delete()
        return redirect('leaderboards_list')

    return render(request, 'leaderboard/delete_leaderboard.html', {'leaderboard': leaderboard})