# Generated by Django 3.2.13 on 2023-10-28 06:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_number', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=200)),
                ('phoneII', models.CharField(max_length=200)),
                ('plate_no', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=255)),
                ('sponsor', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('finish_date', models.DateField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='drivers/')),
            ],
        ),
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('ids', models.AutoField(primary_key=True, serialize=False)),
                ('file_name', models.CharField(max_length=200)),
                ('my_files', models.FileField(upload_to='uploads/')),
            ],
        ),
        migrations.CreateModel(
            name='unknownDriver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('payment_date', models.DateField()),
                ('transaction_type', models.CharField(max_length=255)),
                ('received_from', models.CharField(max_length=255)),
                ('txn_id', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('balance_before', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateField()),
                ('transaction_type', models.CharField(max_length=255)),
                ('received_from', models.CharField(max_length=255)),
                ('txn_id', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('receiver', models.CharField(max_length=200)),
                ('balance_before', models.FloatField()),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LwoBajaji.driver')),
            ],
        ),
        migrations.CreateModel(
            name='Bajaji',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plate_no', models.CharField(max_length=15)),
                ('date_contract', models.DateField()),
                ('status_payment', models.CharField(choices=[('not-paid', 'not-paid'), ('paid-day', 'paid-day'), ('paid-month', 'paid-month')], default='not-paid', max_length=20)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LwoBajaji.driver')),
            ],
        ),
    ]
