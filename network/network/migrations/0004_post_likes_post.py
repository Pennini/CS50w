# Generated by Django 4.2.6 on 2023-11-18 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_alter_post_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes_post',
            field=models.IntegerField(default=0),
        ),
    ]
