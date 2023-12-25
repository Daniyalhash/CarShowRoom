# Generated by Django 4.2.7 on 2023-12-11 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Garage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carShowRoom.car')),
            ],
        ),
        migrations.CreateModel(
            name='CarSpecification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fuel_type', models.CharField(max_length=255)),
                ('engine_horsepower', models.IntegerField()),
                ('engine_torque', models.IntegerField()),
                ('transmission', models.CharField(max_length=255)),
                ('fuel_efficiency', models.DecimalField(decimal_places=2, max_digits=5)),
                ('performance_0_60', models.DecimalField(decimal_places=2, max_digits=5)),
                ('top_speed', models.IntegerField()),
                ('car', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='carShowRoom.car')),
            ],
        ),
        migrations.CreateModel(
            name='CarPricing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('premium_package_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('technology_package_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('special_offers', models.TextField()),
                ('car', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='carShowRoom.car')),
            ],
        ),
        migrations.CreateModel(
            name='CarColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color_image_path', models.ImageField(upload_to='color_images/')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carShowRoom.car')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carShowRoom.color')),
            ],
        ),
    ]