# Generated by Django 4.2.7 on 2023-12-14 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carShowRoom', '0004_user_alter_like_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='garage',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]