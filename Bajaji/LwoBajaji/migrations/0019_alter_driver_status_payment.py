# Generated by Django 3.2.13 on 2023-11-03 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LwoBajaji', '0018_auto_20231103_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='status_payment',
            field=models.CharField(choices=[('not-paid', 'not-paid'), ('paid-day', 'paid-day'), ('paid-week', 'paid-week')], default='not-paid', max_length=20),
        ),
    ]
