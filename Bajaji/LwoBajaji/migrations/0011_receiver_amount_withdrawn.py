# Generated by Django 3.2.13 on 2023-10-31 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LwoBajaji', '0010_payment_receiver'),
    ]

    operations = [
        migrations.AddField(
            model_name='receiver',
            name='amount_withdrawn',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
