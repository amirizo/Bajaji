from django.urls import path 
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.register, name="register"),
    path('login', views.Login, name="login"),
    path('logout', views.logout, name="logout"),
    path('index', views.index, name="index"),
    path('driver_list', views.driver_list, name="driver_list"),
    path('my_store', views.my_store, name="my_store"),
    path('add_driver_form', views.add_driver_form, name="add_driver_form"),
    path('payment', views.payment, name="payment"),
    path('show_file', views.show_file, name="show_file"),
    path('unknown_driver', views.unknown_driver, name="unknown_driver"),
    path('delete_driver', views.delete_driver, name="delete_driver"),
    path('update_driver', views.update_driver, name='update_driver'),
   # path('link_unknown_payment', views.link_unknown_payment, name="link_unknown_payment"),
   path('withdraw_money', views.withdraw_money, name='withdraw_money'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

