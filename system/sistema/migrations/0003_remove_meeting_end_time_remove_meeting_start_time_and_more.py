# Generated by Django 4.2.6 on 2023-12-21 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0002_meeting_report'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='start_time',
        ),
        migrations.AddField(
            model_name='meeting',
            name='duration',
            field=models.IntegerField(default=0),
        ),
    ]