# Generated by Django 3.2.13 on 2023-10-31 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LwoBajaji', '0015_alter_payment_receiver'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bajaji',
            name='driver',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='driver',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='receiver',
            name='user',
        ),
        migrations.DeleteModel(
            name='unknownDriver',
        ),
        migrations.DeleteModel(
            name='Bajaji',
        ),
        migrations.DeleteModel(
            name='Driver',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
        migrations.DeleteModel(
            name='Receiver',
        ),
    ]