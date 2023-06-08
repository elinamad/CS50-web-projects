# Generated by Django 4.2 on 2023-06-01 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_bids_id_alter_comments_id_alter_listings_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bids',
            old_name='id',
            new_name='bid_id',
        ),
        migrations.RenameField(
            model_name='comments',
            old_name='id',
            new_name='comment_id',
        ),
        migrations.RenameField(
            model_name='listings',
            old_name='id',
            new_name='listing_id',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='id',
            new_name='user_id',
        ),
    ]