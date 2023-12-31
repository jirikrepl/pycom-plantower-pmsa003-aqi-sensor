# Generated by Django 3.2.23 on 2023-12-17 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AirQuality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('pm1_0_concentration', models.DecimalField(decimal_places=2, max_digits=5)),
                ('pm2_5_concentration', models.DecimalField(decimal_places=2, max_digits=5)),
                ('pm10_concentration', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]
