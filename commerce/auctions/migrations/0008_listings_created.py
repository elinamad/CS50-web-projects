# Generated by Django 4.2 on 2023-06-02 11:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_listings_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
