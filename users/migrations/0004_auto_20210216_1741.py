# Generated by Django 3.1.2 on 2021-02-16 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210211_2102'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_lat',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='user_lng',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='cto_lat',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='cto_lng',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
