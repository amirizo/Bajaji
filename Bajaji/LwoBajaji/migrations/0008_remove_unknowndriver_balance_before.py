# Generated by Django 3.2.13 on 2023-10-30 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LwoBajaji', '0007_alter_payment_receiver'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unknowndriver',
            name='balance_before',
        ),
    ]