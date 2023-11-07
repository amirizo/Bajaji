from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


# Create your models here.

class Driver(models.Model):
    id_number = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    phoneII = models.CharField(max_length=200)
    plate_no = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    sponsor = models.CharField(max_length=255)
    start_date = models.DateField()
    finish_date = models.DateField()
    image = models.ImageField(upload_to='drivers/', null=True, blank=True)
    
    STATUS_CHOICES = (
        ('not-paid', 'not-paid'),
        ('paid-day', 'paid-day'),
        ('paid-week', 'paid-week'),
    )

    status_payment = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not-paid')



    def __str__(self):
        return self.name

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Bajaji(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    plate_no = models.CharField(max_length=15)
    date_contract = models.DateField()

    def __str__(self):
        return f'{self.driver.name} - {self.plate_no}'


class Receiver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    total_amount_received =  models.DecimalField(max_digits=10, decimal_places=2,  default=0)
    amount_withdrawn = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.user.username


    def update_total_amount_received(self):
        total_received = Payment.objects.filter(receiver=self).aggregate(Sum('amount'))['amount__sum'] or 0
        self.total_amount_received = total_received
        self.save()



class Payment(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    payment_date = models.DateField()
    transaction_type = models.CharField(max_length=255)
    received_from = models.CharField(max_length=255)
    txn_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    receiver = models.ForeignKey( Receiver, on_delete=models.CASCADE)
    balance_before = models.FloatField()
    def __str__(self):
        return f"Payment on {self.payment_date} from {self.received_from} - {self.amount}"


class UnknownDriver(models.Model):
    name = models.CharField(max_length=200)
    payment_date = models.DateField()
    transaction_type = models.CharField(max_length=255)
    received_from = models.CharField(max_length=255)
    txn_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.name


class FileUpload(models.Model):
    ids = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=200)
    my_files = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.file_name



