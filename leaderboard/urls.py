from django.contrib import admin
from django.urls import path, include
import leaderboard.leaderboard_views as leaderboard_views
import leaderboard.user_views as user_views
import leaderboard.option_views as option_views
import leaderboard.entry_views as entry_views

urlpatterns = [
    path('', leaderboard_views.main_view, name='main'),
    
    path('leaderboard/', leaderboard_views.leaderboard_list, name='leaderboards_list'),
    path('leaderboard/<int:leaderboard_id>/', leaderboard_views.leaderboard_detail, name='leaderboard_detail'),
    path('leaderboard/create/', leaderboard_views.create_leaderboard, name='create_leaderboard'),
    path('leaderboard/<int:leaderboard_id>/edit/', leaderboard_views.edit_leaderboard, name='edit_leaderboard'),
    path('leaderboard/<int:leaderboard_id>/delete/', leaderboard_views.delete_leaderboard, name='delete_leaderboard'),
    
    path('leaderboard/<int:leaderboard_id>/entry/add/', entry_views.add_entry, name='add_entry'),
    # path('leaderboard/<int:leaderboard_id>/entry/<int:entry_id>/edit/', entry_views.edit_entry, name='edit_entry'),
    # path('leaderboard/<int:leaderboard_id>/entry/<int:entry_id>/delete/', entry_views.delete_entry, name='delete_entry'),
    
    path('leaderboard/<int:leaderboard_id>/option/add/', option_views.add_option, name='add_option'),
    # path('leaderboard/<int:leaderboard_id>/option/<int:option_id>/edit/', option_views.edit_option, name='edit_option'),
    # path('leaderboard/<int:leaderboard_id>/option/<int:option_id>/delete/', option_views.delete_option, name='delete_option'),

    path('accounts/create_user/', user_views.create_user, name='create_user'),
    path('accounts/profile/', user_views.profile_view, name='profile'),
    path('accounts/edit_profile/', user_views.edit_profile, name='edit_profile'),
    path('accounts/logout/', user_views.logout, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
]