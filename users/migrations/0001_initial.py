# Generated by Django 3.1.2 on 2020-12-28 15:20

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneOTP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=12, unique=True)),
                ('nickname', models.CharField(blank=True, max_length=30, null=True)),
                ('otp', models.CharField(blank=True, max_length=9, null=True)),
                ('validated', models.BooleanField(default=False, help_text='True means user has a validated otp correctly in second API')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('phone', models.CharField(max_length=15, unique=True)),
                ('password1', models.CharField(blank=True, max_length=20, null=True)),
                ('password2', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True, unique=True)),
                ('nickname', models.CharField(blank=True, max_length=50, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_online', models.DateTimeField(blank=True, null=True)),
                ('avatar', models.ImageField(default='default/default.png', upload_to=users.models.user_photos_dir)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
