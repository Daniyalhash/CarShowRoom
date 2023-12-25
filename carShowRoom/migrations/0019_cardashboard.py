# Generated by Django 4.2.7 on 2023-12-20 07:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carShowRoom', '0018_system'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarDashboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carShowRoom.car')),
            ],
        ),
    ]