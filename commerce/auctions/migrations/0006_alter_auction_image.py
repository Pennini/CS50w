# Generated by Django 4.2.5 on 2023-10-10 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_bids_current_bid_alter_bids_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]
