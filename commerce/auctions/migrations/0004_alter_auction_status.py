# Generated by Django 4.2.5 on 2023-10-09 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_auction_category_alter_auction_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='status',
            field=models.CharField(choices=[('open', 'Open'), ('closed', 'Closed')], default='open', max_length=7),
        ),
    ]
