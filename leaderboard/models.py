from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class LeaderboardEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    realise_with = models.ForeignKey('RealiseWith', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}: {self.score}{f" ({self.realise_with.name})" if self.realise_with else ''}"


class Leaderboard(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_leaderboards')
    entries = models.ManyToManyField(LeaderboardEntry)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    shared_with_users = models.ManyToManyField(User, related_name='shared_leaderboards', blank=True)
    public = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def get_top_entries(self, limit=10):
        return self.entries.order_by('-score')[:limit]
    
    def get_page(self, page_number=1, entries_per_page=10):
        start = (page_number - 1) * entries_per_page
        end = start + entries_per_page
        return self.entries.order_by('-score')[start:end]
    
    def get_nb_pages(self, entries_per_page=10):
        return (self.entries.count() // (entries_per_page+1)) + 1

    def have_access(self, user):
        if not user.is_authenticated:
            return False
        elif user.is_superuser:
            return True
        elif self.creator == user:
            return True
        elif self.public:
            return True
        else:
          return self.shared_with_users.filter(id=user.id).exists()
    
    def is_mine(self, user):
        return self.creator == user
    
    def is_public(self):
        return self.public


class RealiseWith(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    belongs_to = models.ForeignKey(Leaderboard, on_delete=models.CASCADE, related_name='realise_with_options')
    
    def __str__(self):
        return self.name