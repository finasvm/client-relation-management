from django.urls import path
from .views import *

urlpatterns = [
    path('home/',Home.as_view(),name='home'),
    path('login/',SignIn.as_view(),name='login'),
    path('addcustomers/',AddCustomer.as_view(),name='addcustomer'),
    path('showcustomer/',ShowCustomers.as_view(),name='showcustomer'),
    path('editcustomer/',EditCustomer.as_view(),name='editcustomer'),
    path('viewnote/',Note.as_view(),name='viewnote'),
    path('delcustomer/',DeleteCustomer.as_view(),name='deletecustomer'),
    path('customereport/',CustomerReport.as_view(),name='customereport'),
    path('logout/',LogOut.as_view(),name='signout'),

]