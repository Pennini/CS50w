# Generated by Django 4.2.6 on 2023-11-16 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_post_likes_follow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(),
        ),
    ]
