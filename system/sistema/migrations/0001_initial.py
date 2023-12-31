# Generated by Django 4.2.6 on 2023-12-13 00:03

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('biography', models.TextField(blank=True, max_length=250, null=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Human Resources', 'Human Resources'), ('Marketing', 'Marketing'), ('Project Management', 'Project Management')], max_length=30)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('meeting_day', models.CharField(choices=[('0', 'Monday'), ('1', 'Tuesday'), ('2', 'Wednesday'), ('3', 'Thursday'), ('4', 'Friday'), ('5', 'Saturday'), ('6', 'Sunday')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Artificial Intelligence', 'Artificial Intelligence'), ('Cybersecurity', 'Cybersecurity'), ('Data Science', 'Data Science'), ('Web Development', 'Web Development')], max_length=30)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('meeting_day', models.CharField(choices=[('0', 'Monday'), ('1', 'Tuesday'), ('2', 'Wednesday'), ('3', 'Thursday'), ('4', 'Friday'), ('5', 'Saturday'), ('6', 'Sunday')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('member', 'Member'), ('trainee', 'Trainee'), ('director', 'Director'), ('leader', 'Leader'), ('vice-president', 'Vice-President'), ('president', 'President')], max_length=30)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('start_day', models.DateTimeField()),
                ('end_day', models.DateTimeField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('category', models.CharField(blank=True, max_length=20, null=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_group', to='sistema.group')),
                ('members', models.ManyToManyField(blank=True, related_name='project_members', to=settings.AUTH_USER_MODEL)),
                ('responsible', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_responsible', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateTimeField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('area', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meeting_area', to='sistema.area')),
                ('group', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meeting_group', to='sistema.group')),
                ('members_present', models.ManyToManyField(blank=True, related_name='meeting_members_present', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=500)),
                ('start_day', models.DateTimeField()),
                ('end_day', models.DateTimeField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('category', models.CharField(blank=True, max_length=20, null=True)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_area', to='sistema.area')),
                ('members_planned', models.ManyToManyField(blank=True, related_name='event_members_planned', to=settings.AUTH_USER_MODEL)),
                ('members_present', models.ManyToManyField(blank=True, default=None, null=True, related_name='event_members_present', to=settings.AUTH_USER_MODEL)),
                ('responsible', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_responsible', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Availabilty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('0', 'Monday'), ('1', 'Tuesday'), ('2', 'Wednesday'), ('3', 'Thursday'), ('4', 'Friday'), ('5', 'Saturday'), ('6', 'Sunday')], max_length=20)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('status', models.IntegerField(choices=[(0, 'Not Available'), (1, 'Medium'), (2, 'Available')], default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availability_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='area',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_area', to='sistema.area'),
        ),
        migrations.AddField(
            model_name='user',
            name='group',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_group', to='sistema.group'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='position',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_position', to='sistema.position'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
