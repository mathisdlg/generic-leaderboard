# Generated by Django 4.2.23 on 2025-07-23 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leaderboardentry',
            name='realise_with',
        ),
        migrations.AlterField(
            model_name='leaderboardentry',
            name='score',
            field=models.CharField(max_length=100),
        ),
        migrations.AddField(
            model_name='leaderboardentry',
            name='realise_with',
            field=models.ManyToManyField(blank=True, to='leaderboard.realisewith'),
        ),
    ]
