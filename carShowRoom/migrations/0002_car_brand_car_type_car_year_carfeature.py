# Generated by Django 4.2.7 on 2023-12-11 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carShowRoom', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='brand',
            field=models.CharField(default='Unknown', max_length=255),
        ),
        migrations.AddField(
            model_name='car',
            name='type',
            field=models.CharField(default='Sedan', max_length=255),
        ),
        migrations.AddField(
            model_name='car',
            name='year',
            field=models.IntegerField(default=2023),
        ),
        migrations.CreateModel(
            name='CarFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry', models.CharField(max_length=255)),
                ('seats', models.CharField(max_length=255)),
                ('sunroof', models.CharField(max_length=255)),
                ('system', models.CharField(max_length=255)),
                ('car', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='carShowRoom.car')),
            ],
        ),
    ]
