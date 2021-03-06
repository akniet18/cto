# Generated by Django 3.1.2 on 2021-01-08 13:35

import cars.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0002_car'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=cars.models.photos_dir)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car_img', to='cars.car')),
            ],
        ),
    ]
