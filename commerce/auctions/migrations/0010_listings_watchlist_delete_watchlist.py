# Generated by Django 4.2 on 2023-06-04 11:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_listings_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='watchlist',
            field=models.ManyToManyField(blank=True, null=True, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Watchlist',
        ),
    ]