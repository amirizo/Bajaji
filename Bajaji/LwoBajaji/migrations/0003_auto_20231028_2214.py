# Generated by Django 3.2.13 on 2023-10-28 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LwoBajaji', '0002_auto_20231028_2213'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driver',
            name='total_bajaji',
        ),
        migrations.AddField(
            model_name='bajaji',
            name='total_bajaji',
            field=models.IntegerField(default=0),
        ),
    ]
