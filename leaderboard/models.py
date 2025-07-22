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
    entries = models.ManyToManyField(LeaderboardEntry)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    def get_top_entries(self, limit=10):
        return self.entries.order_by('-score')[:limit]
    
    def get_page(self, page_number=1, entries_per_page=10):
        start = (page_number - 1) * entries_per_page
        end = start + entries_per_page
        return self.entries.order_by('-score')[start:end]


class RealiseWith(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name