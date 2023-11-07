from . models import *
from django.db.models import Sum


def get_summary_totals():
    total_drivers = Driver.objects.count()
    total_bajaji = Bajaji.objects.count()
    total_unknown_drivers = UnknownDriver.objects.count()

  
    total_amount_received = Receiver.objects.aggregate(Sum('total_amount_received'))['total_amount_received__sum'] or 0



    return {
        'total_drivers': total_drivers,
        'total_bajaji': total_bajaji,
        'total_unknown_drivers': total_unknown_drivers,
    #    'total_income': total_income,
        'total_amount_received': total_amount_received,
    }
