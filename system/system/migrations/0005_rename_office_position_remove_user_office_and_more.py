# Generated by Django 4.2.6 on 2023-11-25 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0004_alter_area_meeting_day_alter_availabilty_day_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Office',
            new_name='Position',
        ),
        migrations.RemoveField(
            model_name='user',
            name='office',
        ),
        migrations.AddField(
            model_name='user',
            name='position',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_position', to='system.position'),
        ),
    ]