# Generated by Django 4.2.5 on 2023-10-10 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auction_date_bids_date_last_bid_comments_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='date_last_bid',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='comments',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
