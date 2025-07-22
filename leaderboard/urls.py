from django.contrib import admin
from django.urls import path, include
import leaderboard.views as leaderboard_views

urlpatterns = [
    path('', leaderboard_views.main_view, name='main'),
    # base connection page for user
    path('account/', include('django.contrib.auth.urls')),
]