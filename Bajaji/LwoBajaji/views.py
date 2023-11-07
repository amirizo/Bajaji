from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import CreateUserform, LoginForm, MyfileUploadForm, PaymentForm, WithDrawForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import *
import json
import pandas as pd
import os
import re
from django.core.exceptions import ValidationError
from datetime import datetime
from django.conf import settings
from django.contrib import messages
from django.db.models import Sum, F
from .utils import get_summary_totals
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404
from django.http import HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db.models import Q






# Create your views here.
# Create your views here....
# -Register
def register(request):
    form =  CreateUserform()

    if request.method == 'GET':
        form = CreateUserform(request.GET)
        if form.is_valid():
            if form.is_valid():
                user = form.save(commit=False)
                user.save() 

                phone_number = form.cleaned_data['phone_number']
                receiver, created = Receiver.objects.get_or_create(user=user, phone_number=phone_number)
            if created:
                receiver.save()

            return redirect('index')
    else:
        form = CreateUserform()
    context = {'form':form}
    return render(request, 'Lwo/register.html', context)


def Login(request):
    if request.method == 'GET':
        form = LoginForm(request, data=request.GET)

        if form.is_valid():
            username = request.GET.get('username')
            password = request.GET.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('index')

    return render(request, 'Lwo/login.html')


def logout(request):
   auth.logout(request)
   return redirect('login')


@login_required(login_url='login')
def index(request):
    total_income = 0 
    total_income = Payment.objects.aggregate(Sum('amount'))['amount__sum'] or 0 

    drivers = Driver.objects.all()
    context = {
        'drivers': drivers,
        'total_income': total_income
    }
    context.update(get_summary_totals())
    return render(request, ('Lwo/index.html'), context)




@login_required(login_url='login')
def driver_list(request):
    total_income = 0 
    total_income = Payment.objects.aggregate(Sum('amount'))['amount__sum'] or 0 

    drivers = Driver.objects.all()

    driver_payments = Payment.objects.values('driver').annotate(total_amount=Sum('amount'))


    for driver in drivers:
        for driver_payment in driver_payments:
            driver_id = driver_payment['driver']
            total_payment = driver_payment['total_amount']
            
            if driver.id == driver_id:
                driver.total_payment = total_payment
                if total_payment > 0:
                    driver.status_payment = 'paid'
                    driver.payment_status_css = 'paid'
                else:
                    driver.status_payment = 'not-paid'
                    driver.payment_status_css = 'not-paid'
            driver.save()
    
    form = WithDrawForm()

    context = {
        'drivers': drivers,
        'total_income': total_income,
        'form': form,
    }
    context.update(get_summary_totals())
    return render(request, ('Lwo/driver_list.html'), context)

def withdraw_money(request):
    if request.method == 'POST':
        form = WithDrawForm(request.POST)
        receiver = Receiver.objects.get(user=request.user)

        if form.is_valid():
            amount_to_withdraw = form.cleaned_data['amount_to_withdraw']

            if amount_to_withdraw <= receiver.total_amount_received:
                receiver.amount_withdrawn += amount_to_withdraw
                receiver.save()

                receiver.total_amount_received -= amount_to_withdraw
                receiver.save()

                return redirect()
            else:
                return HttpResponse('Insufficient funds for withdrawal.')
    else:
        form = WithDrawForm

    context = {
        'form': form
    }
    context.update(get_summary_totals())
    return render(request, 'Lwo/withdraw_money.html', context)




def add_driver_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        start_date = request.POST.get('start_date')
        finish_date = request.POST.get('finish_date')
        plate_no = request.POST.get('plate_no')
        address = request.POST.get('address')
        text = request.POST.get('text')
        phoneII = request.POST.get('phone2')
        image = request.FILES.get('image')

        if image:
            fs = FileSystemStorage()
            file_name = fs.save(image.name, image)
            image_url = fs.url(file_name)
        else:
            image = '/media/avatar.png' 

        

        new_driver = Driver(
            name=name,
            phone=phone,
            start_date=start_date,
            finish_date=finish_date,
            plate_no=plate_no,
            address=address,
            phoneII=phoneII,
            sponsor=text,
            image=image,
        )
        new_driver.save()

        new_bajaji = Bajaji(
            driver=new_driver,
            plate_no=plate_no,
            date_contract=start_date
        )
        new_bajaji.save()
    return JsonResponse(('driver was added succesfully'), safe=False)

def delete_driver(request):
    if request.method == 'GET':
        driverId = request.GET.get('driverId')
        print('driverId:', driverId)
        
        try:
            drivers = Driver.objects.filter(id=driverId)
            
            if drivers.exists():
                drivers.delete()
                return JsonResponse({'deleted': True})
            else:
                return JsonResponse({'deleted': False})
        except Driver.DoesNotExist:
            return JsonResponse({'deleted': False})
    else:
        return JsonResponse({'deleted': False, 'error': 'Invalid request method'})


def update_driver(request):
    if request.method == 'POST':
        driverId = request.GET.get('driverId')
        print('driverId:', driverId)

        name = request.GET.get('name')
        phone = request.GET.get('phone')
        start_date = request.GET.get('start_date')
        finish_date = request.GET.get('finish_date')
        phone2 = request.GET.get('phone2')
        plate_no = request.GET.get('plate_no')
        text = request.GET.get('text')
        address = request.GET.get('address')
        image = request.FILES.get('image')

        if image:
            fs = FileSystemStorage()
            file_name = fs.save(image.name, image)
            image_url = fs.url(file_name)
        else:
            image = '/media/avatar.png' 

        
    
        try:
            driver = Driver.objects.get(id=driverId)

            driver.name = name
            driver.phone = phone
        #   driver.start_date = start_date
        #   driver.finish_date = finish_date
            driver.phoneII = phone2
            driver.plate_no = plate_no
            driver.sponsor = text
            driver.address = address
            driver.image = image
                
            driver.save()
            return JsonResponse({'success': True})
        except Driver.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Driver not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})






@login_required(login_url='login')
def my_store(request):
    total_income = 0 
    total_income = Payment.objects.aggregate(Sum('amount'))['amount__sum'] or 0 



    bajajis = Bajaji.objects.all()
    context = {
        'bajajis':bajajis,
        'total_income': total_income,
    }
    form = WithDrawForm()

    context.update(get_summary_totals())
    return render(request, ('Lwo/my_store.html'), context)








@login_required(login_url='login')
def show_file(request):
    all_data = FileUpload.objects.all()
    context = {
        'data': all_data
    }
    context.update(get_summary_totals())
    return render(request, ('Lwo/view.html'), context)

def read_excel_file(file):
    try:
        excel_data = pd.read_excel(file)

        excel_data = excel_data.dropna(how='all')


        selected_columns = ["", "SENDER", "RECEIVER", "TX_ID", "Service_Type", "AMOUNT", "PRE_BAL", "POST_BAL", "TRANS_DATE", "TRANSFER_TIME"]
        excel_data = excel_data[selected_columns]

        return excel_data
    except Exception as e:
        print(str(e))
        return None


@login_required(login_url='login')
def payment(request):
    unique_payment_dates = Payment.objects.values('payment_date').distinct()
    total_income = 0
    total_received_by_drivers = 0

    if request.method == 'POST':
        cform = MyfileUploadForm(request.POST, request.FILES)

        if cform.is_valid():
            files = cform.cleaned_data['files']
            FileUpload(my_files=files).save()
            excel_data = pd.read_excel(files)

            existing_tx_ids = set(Payment.objects.values_list('txn_id', flat=True))
            new_data = pd.read_excel(files)
            new_payments = []
            existing_driver_numbers = set(Driver.objects.values_list('phone', flat=True))
            existing_driver_numbers.update(Driver.objects.values_list('phoneII', flat=True))

            for index, row in excel_data.iterrows():
                cm_number = row['SENDER']
                receiver_number = row['RECEIVER']
                txn_id = row['TX_ID']
                payment_date = row['TRANS_DATE']
                transaction_type = row['Service_Type']
                received_from = row['SENDER']
                amount = row.get('AMOUNT', 0)
                balance_before = row['PRE_BAL']

                current_balance = 0
                drivers = Driver.objects.filter(Q(phone=cm_number) | Q(phoneII=cm_number))



                receiver_number = row['RECEIVER']
                txn_id = row['TX_ID']
                payment_date = row['TRANS_DATE']
                transaction_type = row['Service_Type']
                received_from = row['SENDER']
                amount = row.get('AMOUNT', 0)
                balance_before = row['PRE_BAL']

                if 'Service_Type' in row and row['Service_Type'].lower() == 'usage':
                    usage_amount = row.get('AMOUNT', 0)
                    try:
                        receiver = Receiver.objects.get(phone_number=received_from)
                    except Receiver.DoesNotExist:
                        receiver = None


                    if receiver:
                        receiver.amount_withdrawn += usage_amount
                        receiver.total_amount_received -= usage_amount
                        receiver.save()
                        messages.success(request, f'Kiwango cha {usage_amount} kimeondolewa kutoka kwa Receiver')

                for driver in drivers:
                    total_income += amount
                    current_balance = 0

                    

                    try:
                        receiver = Receiver.objects.get(phone_number=receiver_number)
                    except Receiver.DoesNotExist:
                        receiver = None

                    if driver and receiver:
                        current_balance += amount

                        payment = Payment(
                            driver=driver,
                            payment_date=payment_date,
                            transaction_type=transaction_type,
                            received_from=received_from,
                            txn_id=txn_id,
                            amount=amount,
                            receiver=receiver,
                            balance_before=current_balance
                        )
                        payment.save()
                        receiver.update_total_amount_received()

                existing_unknown = UnknownDriver.objects.filter(name=received_from, payment_date=payment_date).first()
                if existing_unknown is not None:
                    existing_unknown.amount += amount
                else:
                    if not drivers:
                        unknown_driver = UnknownDriver(
                            name=received_from,
                            payment_date=payment_date,
                            transaction_type=transaction_type,
                            received_from=received_from,
                            txn_id=txn_id,
                            amount=amount,
                        )
                        unknown_driver.save()
                        messages.info(request, f'Namba za dereva {cm_number} hazijulikani.')
            Payment.objects.bulk_create(new_payments)

    total_income = total_received_by_drivers

    selected_date = request.GET.get('payment_date')

    if selected_date == 'all':
        payment_date = datetime.now().date()
        payments = Payment.objects.filter(payment_date=payment_date)
    else:
        if selected_date:
            try:
                payment_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
                payments = Payment.objects.filter(payment_date=payment_date)
            except ValueError:
                payments = Payment.objects.all()
        else:
            payments = Payment.objects.all()

    total_income = Payment.objects.aggregate(Sum('amount'))['amount__sum'] or 0

    all_data = FileUpload.objects.all()
    form = WithDrawForm()
    context = {
        'payments': payments,
        'form': MyfileUploadForm(),
        'data': all_data,
        'unique_payment_dates': unique_payment_dates,
        'total_income': total_income,
    }
    context.update(get_summary_totals())
    return render(request, 'Lwo/payments.html', context)


@login_required(login_url='login')
def unknown_driver(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            phone = form.cleaned_data["phone"]
            phone11 = form.cleaned_data["phone11"]

            unknown_driver_payments = UnknownDriver.objects.filter(received_from=phone11)

            for unknown_payment in unknown_driver_payments:
                try:
                    driver = Driver.objects.get(name=name, phone=phone)
                except Driver.DoesNotExist:
                    return render(request, "error.html", {"message": "Hakuna dereva mwenye data kama hiyo"})

                if request.user.is_authenticated:
                    shinuna = request.user
                else:
                    shinuna = None

                if shinuna:
                    try:
                        receiver = Receiver.objects.get(user=shinuna, phone_number=phone11)
                    except Receiver.DoesNotExist:
                        receiver = None
                else:
                    receiver = None

                new_payment = Payment(
                    driver=driver,
                    payment_date=unknown_payment.payment_date,
                    transaction_type=unknown_payment.transaction_type,
                    received_from=phone11,
                    txn_id=unknown_payment.txn_id,
                    amount=unknown_payment.amount,
                    receiver=receiver,  # Tumia 'receiver' uliopata au None
                    balance_before=0
                )
                new_payment.save()
                unknown_payment.delete()

            return redirect("payment")
    else:
        form = PaymentForm()


    unknown_drivers = UnknownDriver.objects.all()
    context = {
        'unknown_drivers': unknown_drivers,
        "form": form
    }
    context.update(get_summary_totals())
    return render(request, 'Lwo/unknown_driver.html', context)
