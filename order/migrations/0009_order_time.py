# Generated by Django 3.1.2 on 2021-02-19 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_auto_20210217_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='time',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]